#!/usr/bin/env python

import time
from datetime import datetime
from microsvax.service import timer
from microsvax.service import event
from microsvax.service import rpc
from microsvax import mservice


@timer(seconds=2)
def every2():
    mservice.send_event("test1", "2 => {}".format(datetime.now()))


@event(name="test2")
def observe(value):
    print("2 recoit : {}".format(value))


@timer(seconds=5)
def rpc_test():
    result = mservice.call_rpc("add.numbers", 12, 8)
    print("rpc result = {}".format(result))


time.sleep(15)
mservice.stop()
