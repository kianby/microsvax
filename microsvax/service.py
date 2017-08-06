#!/usr/bin/env python

import asyncio
from threading import Thread
import aioredis
import time
import pickle
from microsvax import CoroutineInfo
from microsvax import CoroutineKind
from microsvax import mservice


def timer(seconds):

    async def coroutine(func, coroutine_info):
        while not coroutine_info.must_stop:
            func()
            await asyncio.sleep(seconds)

    def start_loop(loop, func, coroutine_info):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine(func, coroutine_info))
        loop.stop()
        loop.close()

    def wrapper(func):
        loop = asyncio.new_event_loop()
        coroutine_info = CoroutineInfo(CoroutineKind.TIMER, loop)
        thread = Thread(target=start_loop, args=(loop, func, coroutine_info))
        coroutine_info.thread = thread
        thread.start()
        mservice.register(coroutine_info)
    return wrapper


def rpc(name):

    async def coroutine(func, event_channel, coroutine_info):
        while await event_channel.wait_message():
            if coroutine_info.must_stop:
                break
            msg = await event_channel.get()
            args = pickle.loads(msg)
            print('rpc call received {}'.format(args))
            result = func(*args)
            mservice.set_value("res-{}".format(name), result)

    async def monitor(r, admin_channel, coroutine_info):
        await admin_channel.wait_message()
        r.close()
        await r.wait_closed()

    async def start_channels(loop, func, name, coroutine_info):
        r = await aioredis.create_redis(('localhost', 6379))
        event_channel, admin_channel = await r.subscribe(name, coroutine_info.id)

        await asyncio.gather(monitor(r, admin_channel, coroutine_info),
                             coroutine(func, event_channel, coroutine_info))

    def start_loop(loop, func, coroutine_info):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_channels(loop, func, name, coroutine_info))
        loop.stop()
        loop.close()

    def wrapper(func):
        print(name)
        loop = asyncio.new_event_loop()
        coroutine_info = CoroutineInfo(CoroutineKind.RPC, loop)
        thread = Thread(target=start_loop, args=(loop, func, coroutine_info))
        coroutine_info.thread = thread
        thread.start()
        mservice.register(coroutine_info)
    return wrapper


def event(name):

    async def coroutine(func, event_channel, coroutine_info):
        while await event_channel.wait_message():
            if coroutine_info.must_stop:
                break
            msg = await event_channel.get(encoding='utf-8')
            func(msg)

    async def monitor(r, admin_channel, coroutine_info):
        await admin_channel.wait_message()
        r.close()
        await r.wait_closed()

    async def start_channels(loop, func, name, coroutine_info):
        r = await aioredis.create_redis(('localhost', 6379))
        event_channel, admin_channel = await r.subscribe(name, coroutine_info.id)

        await asyncio.gather(monitor(r, admin_channel, coroutine_info),
                             coroutine(func, event_channel, coroutine_info))

    def start_loop(loop, func, coroutine_info):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_channels(loop, func, name, coroutine_info))
        loop.stop()
        loop.close()

    def wrapper(func):
        loop = asyncio.new_event_loop()
        coroutine_info = CoroutineInfo(CoroutineKind.EVENT, loop)
        thread = Thread(target=start_loop, args=(loop, func, coroutine_info))
        coroutine_info.thread = thread
        thread.start()
        mservice.register(coroutine_info)
    return wrapper
