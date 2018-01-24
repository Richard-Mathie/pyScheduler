TaskScheduler
=============

scheduler schedules python tasks to run at some delay time later.

Usage
-----

install

::

    pip install TaskScheduler

run some tasks some time later

::

    from scheduler import Scheduler


    def hello_world(words):
        print "Hello World! ", words


    s = Scheduler()
    s.daemon = True  # so the thread plays nice with shut down

    # Add a task before starting the execution thread
    s.schedule_task(5, hello_world, (" 5 seconds later",))

    # start the execution thread
    s.start()

    # Add more tasks
    task = s.schedule_task(3, hello_world, ("Another Task",))


    # reschedule a task
    task.delay = 4
    s.reschedule_task(task, )

    # delete a task
    s.remove_task(task)

