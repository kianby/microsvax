#!/usr/bin/env python

from enum import Enum
import time
import redis
import pickle


class CoroutineKind(Enum):
    UNDEFINED = 0
    TIMER = 1
    EVENT = 2
    RPC = 3


class CoroutineInfo:

    def __init__(self, kind, loop):
        self.loop = loop
        self.running = True
        self.must_stop = False
        self.id = None
        self.kind = kind

    def wait_until_stopped(self):
        self.must_stop = True
        self.thread.join()
        self.running = False


class Microservice:

    def __init__(self):
        self.id = 'MSVC-{}'.format(time.time())
        self.coroutines = []

    def register(self, coroutine_info):
        coroutine_id = '%s-%s' % (self.id, coroutine_info.thread.ident)
        print('Register coroutine {}'.format(coroutine_id))
        coroutine_info.id = coroutine_id
        self.coroutines.append(coroutine_info)

    def stop(self):
        for coroutine_info in self.coroutines:
            coroutine_info.must_stop = True
            if coroutine_info.kind in (CoroutineKind.EVENT, CoroutineKind.RPC):
                self.send_event(coroutine_info.id, "STOP")
        for coroutine_info in self.coroutines:
            coroutine_info.wait_until_stopped()

    def send_event(self, name, value):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish(name, value)

    def set_value(self, name, value):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        # TODO utiliser setx avec un timeout pour ne pas pourrir redis
        r.set(name, value)

    def call_rpc(self, name, *args):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        req_id = '{}-{}'.format(self.id, time.time())
        args = (req_id,) + args
        value = pickle.dumps(args)
        r.publish(name, value)
        result = None
        # TODO gerer un timeout sur l'appel
        result_key = "res-{}-{}".format(name,req_id)
        for i in range(5):
            time.sleep(1)
            if r.exists(result_key):
                result = r.get(result_key)
                r.delete(result_key)
                break
        return pickle.loads(result)


mservice = Microservice()
