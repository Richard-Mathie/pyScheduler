#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:40:23 2018

@author: richard
"""
from scheduler import Scheduler
from time import time


def test_init():
    s = Scheduler()
    assert s is not None


def test_scheduler():

    def hello_task(ts):
        print 'hello world, ', time() - ts

    s = Scheduler()
    s.daemon = True

    try:
        s.schedule_task(5, hello_task, (time() + 5,))
        s.start()

        for i in range(10):
            delay = i*0.1 + 1
            s.schedule_task(delay, hello_task, (time() + delay,))
      
    except (KeyboardInterrupt, SystemExit):
      print '\n! Received keyboard interrupt, quitting threads.'
      s.cancel()
      s.join()
      print 'threads closed'

