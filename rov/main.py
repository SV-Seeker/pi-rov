import signal as signals

import messages
from config import config
from curio import SignalQueue, TaskGroup, run, spawn, tcp_server  # Queue, CancelledError
from feeds import ClientStreamFeed
from logs import setup_logging
from tasks import ControlTask, HeartbeatTask, StatusTask

logger = setup_logging(__name__)


# TODO: convert all this into a class that is configurable
# Make the messaging layer agnostic?
#

feed = ClientStreamFeed()
out_feed = ClientStreamFeed()


async def connection_handler(client, addr):
    logger.info('connection from %s', addr)
    async with client:
        client_stream = client.as_stream()
        async with TaskGroup(wait=any) as workers:
            # connect client stream to main feed
            await workers.spawn(out_feed.outgoing, client_stream)
            await workers.spawn(feed.incoming, client_stream)
            # TODO: incoming feed message parsing

        # May not need this
        await feed.publish(messages.EXIT)
    logger.info('connection lost %s', addr)


rov_tasks = []


def add_task(Task):
    task = Task.run()
    rov_tasks.append(task)


add_task(HeartbeatTask)
add_task(StatusTask)
add_task(ControlTask)


async def server(host, port):
    # Server task groups
    async with TaskGroup() as group:
        await group.spawn(feed.dispatcher)
        await group.spawn(out_feed.dispatcher)
        await group.spawn(tcp_server, host, port, connection_handler)

        for rov_task in rov_tasks:
            await group.spawn(rov_task, out_feed)


async def main(host, port):
    async with SignalQueue(signals.SIGHUP, signals.SIGTERM) as close_signals:
        logger.info('Starting the server')
        serv_task = await spawn(server, host, port)
        # Stop here and wait for any of the close signals
        signal = await close_signals.get()
        logger.info('Server shutting down: %s', signal)
        # cancle all server tasks
        await serv_task.cancel()


if __name__ == '__main__':
    # from curio.debug import schedtrace
    # run(main('', 9000), with_monitor=True, debug=schedtrace)
    try:
        run(main('', config.get('port')))
    except KeyboardInterrupt:
        pass
