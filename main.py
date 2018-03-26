import signal as signals
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

from feeds import ClientStreamFeed
import messages
from config import config


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

feed = ClientStreamFeed()


async def connection_handler(client, addr):
    logger.info('connection from %s', addr)
    async with client:
        client_stream = client.as_stream()
        async with TaskGroup(wait=any) as workers:
            await workers.spawn(feed.outgoing, client_stream)
            await workers.spawn(feed.incoming, client_stream)

        # May not need this
        await feed.publish(messages.EXIT)
    logger.info('connection lost %s', addr)


rov_tasks = []
def add_task(Task):
    task = Task.run()
    rov_tasks.append(task)


from tasks import ControlTask, HeartbeatTask, StatusTask

add_task(HeartbeatTask)
add_task(StatusTask)
add_task(ControlTask)


async def server(host, port):
    async with TaskGroup() as group:
        await group.spawn(feed.dispatcher)
        await group.spawn(tcp_server, host, port, connection_handler)

        for rov_task in rov_tasks:
            await group.spawn(rov_task, feed)


async def main(host, port):
    async with SignalQueue(signals.SIGHUP, signals.SIGTERM) as close_signals:
        logger.info('Starting the server')
        serv_task = await spawn(server, host, port)
        signal = await close_signals.get()
        logger.info('Server shutting down: %s', signal)
        await serv_task.cancel()


if __name__ == '__main__':
    # from curio.debug import schedtrace
    # run(main('', 9000), with_monitor=True, debug=schedtrace)
    try:
        run(main('', config.get('port')))
    except KeyboardInterrupt:
        pass
