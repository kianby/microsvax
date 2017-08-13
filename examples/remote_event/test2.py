#!/usr/bin/env python

import sys
sys.path.append('../..')

import time
from datetime import datetime
from microsvax.service import event
from microsvax import mservice


@event(name="ping")
def get_ping(value):
    print("Received remotely => {}".format(value))


time.sleep(10)
mservice.stop()
