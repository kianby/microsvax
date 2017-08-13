#!/usr/bin/env python

import sys
sys.path.append('../..')

import time
import random
from microsvax.service import timer
from microsvax.service import rpc
from microsvax import mservice


@timer(seconds=1)
def compute1():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    result = mservice.call_rpc(3, "add.numbers", a, b)
    print("[REMOTE 1] => {} + {} = {}".format(a, b, result))


@timer(seconds=1)
def compute2():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    result = mservice.call_rpc(3, "add.numbers", a, b)
    print("[REMOTE 2] => {} + {} = {}".format(a, b, result))


time.sleep(10)
mservice.stop()
