from time import time
from threading import Thread, Event, Lock
from Queue import PriorityQueue
from Queue import Empty as QEmpty
import itertools


class Task(object):
    def __init__(self, delay, function, args=(), kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.delay = delay

    def call(self):
        return self.function(*self.args, **self.kwargs)

    def scheduel_at(self):
        return time() + self.delay


class Scheduler(Thread):

    def null_fun(*args, **kwargs):
        pass

    nulltask = Task(0, null_fun)

    def __init__(self):
        Thread.__init__(self)
        self.entry_finder = {}
        self.tasks = PriorityQueue()

        self.finish = Event()
        self.new_task = Event()
        self.run_to_compleation = False

        self.count_lock = Lock()
        self.counter = itertools.count()

    def remove_task(self, task):
        try:
            entry = self.entry_finder.pop(task)
            entry[-1] = self.nulltask
            return True
        except KeyError:
            return False

    def add_task(self, task):
        timestamp = task.scheduel_at()
        if timestamp:
            with self.count_lock:
                count = next(self.counter)
                entry = [timestamp, count, task]
                self.entry_finder[task] = entry
                self.tasks.put(entry)
            self.new_task.set()

    def schedule_task(self, *args, **kwargs):
        task = Task(*args, **kwargs)
        self.add_task(task)
        return task

    def reschedule_task(self, task, add_task=True):
        """reschedule task to another execution time
        
        setting `add_task` to `True` (default) will re add the task
        even if it has allready executed. Else it is too late to 
        reschedule the task
        """
        if self.remove_task(task) or add_task:
            self.add_task(task)

    def cancel(self):
        """Stop the scheduler if it hasn't finished yet"""
        self.finish.set()
        self.new_task.set()

    def _continue(self):
        """Returns True if the event loop should continue"""
        return (not self.finish.is_set() or
                (self.run_to_compleation and not self.tasks.empty()))

    def run(self):
        self.new_task.clear()

        while self._continue():
            try:
                timestamp, count, task = self.tasks.get(timeout=1)
                # use an event to test for new tasks
                if self.new_task.wait(timestamp - time()):
                    self.tasks.put((timestamp, count, task))
                    self.new_task.clear()
                else:
                    if task is not self.nulltask:
                        del self.entry_finder[task]
                        task.call()
            except QEmpty:
                self.new_task.wait(10)

