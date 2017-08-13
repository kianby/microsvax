#!/usr/bin/env python

import sys
sys.path.append('../..')

import time
import random
from microsvax.service import timer
from microsvax.service import rpc
from microsvax import mservice


@timer(seconds=1)
def compute_every_3_seconds():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    result = mservice.call_rpc("add.numbers", a, b)
    print("{} + {} = {}".format(a, b, result))


@rpc(name="add.numbers")
def add_number(a, b):
    return a + b


time.sleep(10)
mservice.stop()
