#!/usr/bin/env python

import sys
sys.path.append('../..')

import time
from datetime import datetime
from microsvax.service import timer
from microsvax import mservice


@timer(seconds=1)
def every1():
    value = datetime.now()
    print('date1 {}'.format(value))


@timer(seconds=3)
def every3():
    value = datetime.now()
    print('date3 {}'.format(value))


time.sleep(10)
mservice.stop()
