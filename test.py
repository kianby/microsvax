#!/usr/bin/env python

import asyncio
import time
from datetime import datetime
from microsvax.service import timer
from microsvax.service import event
from microsvax import mservice


@timer(seconds=2)
def every2():
    print('send PING zero')
    mservice.send_event("ping", 0)


@timer(seconds=1)
def every1():
    value = datetime.now()
    print('send date {}'.format(value))
    mservice.send_event("dateevent", value)


@event(name="dateevent")
def get_date(value):
    print("receive and forward date {}".format(value))
    mservice.send_event("ping", value)


@event(name="ping")
def get_ping(value):
    print("receive ping {}".format(value))


time.sleep(10)
mservice.stop()
