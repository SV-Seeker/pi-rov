import logging

from curio import CancelledError, Queue

logger = logging.getLogger(__name__)


class Feed:
    def __init__(self, *args, **kwargs):
        self.queue = Queue()
        self.subscribers = set()

    async def dispatcher(self):
        """Whenever queue is hydrated push it to all subscribers"""
        async for msg in self.queue:
            for queue in self.subscribers:
                await queue.put(msg)

    async def publish(self, msg):
        await self.queue.put(msg)

    # Outgoing handling
    async def outgoing(self, *args, **kwargs):
        queue = Queue()
        try:
            self.subscribers.add(queue)
            async for msg in queue:
                # Do we need to write back? seperate queue for
                msg = self.prepare_outgoing(msg)
                await self.consume_message(msg, *args, **kwargs)
        finally:
            self.subscribers.discard(queue)

    def prepare_outgoing(self, msg):
        return msg

    async def consume_message(self, *args, **kwargs):
        """return an awaitable write endpoint"""
        raise NotImplementedError()

    # Incoming handling
    async def incoming(self, *args, **kwargs):
        try:
            async for msg in self.feed_messages(*args, **kwargs):
                msg = self.prepare_incoming(msg)
                # Do we want to do this? how do we disable removing the echo response?
                await self.publish(msg)
        except CancelledError:
            # TODO handle cancel gracefully
            raise

    def prepare_incoming(self, msg):
        return msg

    def feed_messages(self, *args, **kwargs):
        """must return an asynchronous iterator"""
        raise NotImplementedError()


class ClientStreamFeed(Feed):

    async def consume_message(self, msg, client_stream):
        await client_stream.write(msg)

    def feed_messages(self, client_stream):
        return client_stream
