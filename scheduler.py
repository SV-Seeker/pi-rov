import logging
import functools
from sched import scheduler, time


logger = logging.getLogger(__name__)


class LoopScheduler:
    def __init__(self):
        self.scheduler = scheduler(time.time, time.sleep)
        self.callbacks = {}
        self.loops = []

    def add_loop(self, loop):
        self.loops.append(loop)

    def setup(self):
        logger.info('setting up loops')
        try:
            [loop.setup() for loop in self.loops]
        except Exception as e:
            logger.error('Error setting up loops')
            raise e
        [self.add(*loop.get_add_parameters()) for loop in self.loops]

    def add(self, callback, loop_time, importance=1, *args, **kwargs):
        callback_hash = hash(callback)
        # create new wrapped callback and register it

        @functools.wraps(callback)
        def wrapped_func(*args, **kwargs):
            # measure the time it takes to run task and subtract that from the
            # loop_time
            pre_callback = time.time()
            callback(*args, **kwargs)
            post_callback = time.time()
            new_next_schedule = max(0, loop_time - (post_callback - pre_callback))
            # start the loop over
            event = self.scheduler.enter(
                new_next_schedule, importance, wrapped_func)
            # set new event
            if self.callbacks.get(callback_hash, None):
                self.callbacks[callback_hash]['event'] = event

        event = self.scheduler.enter(loop_time, importance, wrapped_func)

        self.callbacks.update({
            callback_hash: {
                'func': wrapped_func,
                'event': event
            }
        })

    def remove(self, callback):
        # This doesn't work yet
        lookup = hash(callback)
        # Cancel next event
        event = None
        try:
            event = self.callbacks[lookup].get('event', None)
        except KeyError:
            logger.info('event already removed')
        if event:
            logger.warning(event)
            self.scheduler.cancel(event)
            # remove registered callback
            del self.callbacks[lookup]

    @property
    def time_till_next(self):
        now = time.time()
        event_times = [event.time for event in self.scheduler.queue]
        return max((min(*event_times) - now), 0)

    def run(self, **kwargs):
        self.scheduler.run(**kwargs)
