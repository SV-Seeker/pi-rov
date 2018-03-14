import signal
import logging

from curio import (
    run,
    spawn,
    tcp_server,
    SignalQueue,
    TaskGroup,
    Queue,
    CancelledError
)
# from curio.socket import client


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

command_queue = Queue()
reply_queue = Queue()
subscribers = set()


async def dispatcher():
    async for msg in command_queue:
        for queue in subscribers:
            await queue.put(msg)


async def publish(msg):
    await command_queue.put(msg)


async def outgoing(client_stream):
    queue = Queue()
    try:
        subscribers.add(queue)
        async for msg in queue:
            # Do we need to write back? seperate queue for
            await client_stream.write(msg)
    finally:
        subscribers.discard(queue)


async def incoming(client_stream):
    try:
        async for line in client_stream:
            # key is wat
            try:
                key, command = line.split(b':')
            except ValueError:
                logger.error('malformed message: %s', line)
            else:
                # TODO: possibly swap to command queue? naw
                # await publish((key, command))
                await publish(command)
    except CancelledError:
        await client_stream.write(b'exit')
        raise


async def connection_handler(client, addr):
    logger.info('connection from %s', addr)
    async with client:
        client_stream = client.as_stream()
        # await
        async with TaskGroup(wait=any) as workers:
            await workers.spawn(outgoing, client_stream)
            await workers.spawn(incoming, client_stream)

        await publish(b'exit')
    logger.info('connection lost %s', addr)


rov_tasks = []
def add_task(Task):
    task = Task.run()
    rov_tasks.append(task)

from tasks import HeartbeatTask, StatusTask

add_task(HeartbeatTask)
add_task(StatusTask)

async def server(host, port):
    async with TaskGroup() as group:
        await group.spawn(dispatcher)
        await group.spawn(tcp_server, host, port, connection_handler)

        for rov_task in rov_tasks:
            # import ipdb; ipdb.set_trace()
            await group.spawn(rov_task, publish)

async def main(host, port):
    async with SignalQueue(signal.SIGHUP) as restart:
        while True:
            logger.info('Starting the server')
            serv_task = await spawn(server, host, port)
            await restart.get()
            logger.info('Server shutting down')
            await serv_task.cancel()


if __name__ == '__main__':
    from curio.debug import schedtrace
    # run(main('', 9000), with_monitor=True, debug=schedtrace)
    run(main('', 9000))
