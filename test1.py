#!/usr/bin/env python

import time
from datetime import datetime
from microsvax.service import timer
from microsvax.service import event
from microsvax.service import rpc
from microsvax import mservice


@timer(seconds=2)
def every2():
    mservice.send_event("test2", "1 => {}".format(datetime.now()))


@event(name="test1")
def observe(value):
    print("1 recoit : {}".format(value))


@rpc(name="add.numbers")
def add_number(a, b):
    return a + b


time.sleep(15)
mservice.stop()
