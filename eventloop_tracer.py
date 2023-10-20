from google.appengine.ext import ndb
from six import wraps
import os
import collections

class ELObserver(ndb.eventloop.EventLoop):
    def __init__(self):
        super(ELObserver, self).__init__()

    def __setattr__(self, arg_name, value):
        if arg_name == 'current':
            value = DequeueObserver()

        if arg_name == 'rpcs':
            value = DictObserver()
   
        return super(ELObserver, self).__setattr__(arg_name, value)

    def __getattr__(self, arg_name):
        return super(ELObserver, self).__getattr__(arg_name)

class DequeueObserver(collections.deque):

    def __init__(self):
        super(DequeueObserver, self).__init__()

    def append(self, __x):
        print(self.add_log(__x))
        super(DequeueObserver, self).append(__x)
        print(self.current_queue_log())

    def popleft(self):
        val = super(DequeueObserver, self).popleft()
        print(self.pop_log(val))
        print(self.current_queue_log())
        return val

    def format_dequeu_object(self, __x):
        if __x[0].__name__ ==  "_on_future_completion":
            return "on_future_completion running after: {}".format(__x[1][0]._info)
        else:
            return "{}".format(__x[0].__self__._info)

    def format_dequeue_objects(self):
        lst = [self.format_dequeu_object(__x) for __x in self]
        return lst

    def current_queue_log(self):
        return "$$$$$$$$ QUEUE: {} $$$$$$$$".format(self.format_dequeue_objects())
    
    def add_log(self, __x):
        return "----Added to queue: {}".format(self.format_dequeu_object(__x))
    
    def pop_log(self, val):
        return "---executing: {}".format(val[0].__self__._info)
        


class DictObserver(dict):
    def __setitem__(self, key, value):
        print(self.set_item_log())
        super(DictObserver, self).__setitem__(key, value)

    def __delitem__(self, key):
        print(self.del_item_log())
        super(DictObserver, self).__delitem__(key)

    def set_item_log(self, key, value):
        return "///////// In RPC queue set_item: {}, ----Value: {}".format(key, value[0].__self__)

    def del_item_log(self, key):
        return "//////// In PRC removbe item: {}".format(key)

class ELTracer(object):
    def __init__(self, log_at_end = False):
        self.log_at_end = log_at_end

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with self:
                return f(*args, **kwargs)
        return wrapper

    def __enter__(self):
        self._intercept_event_loop(self.log_at_end)
        return self

    def __exit__(self, *args):
        self._release_event_loop()

    @staticmethod
    def _intercept_event_loop():
        os.environ['__EVENT_LOOP__'] = '1'
        ndb.eventloop._state.event_loop = ELObserver()

    @staticmethod
    def _release_event_loop():
        os.environ['__EVENT_LOOP__'] = None
        ndb.eventloop._state.event_loop = ndb.eventloop.EventLoop()

