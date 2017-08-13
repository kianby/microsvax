#!/usr/bin/env python

import sys
sys.path.append('../..')

import time
from datetime import datetime
from microsvax.service import timer
from microsvax.service import event
from microsvax import mservice


@timer(seconds=1)
def every1():
    value = datetime.now()
    print('Ping => {}'.format(value))
    mservice.send_event("ping", value)


@event(name="ping")
def get_ping(value):
    print("Received locally => {}".format(value))


time.sleep(10)
mservice.stop()
