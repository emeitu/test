# -*- coding: utf-8 -*-

"""
	zookeeper client tool
	author: xing.dong
"""

import zookeeper
from datetime import datetime
import threading
import json
import sys
#ZOOKEEPER_SERVERS = "192.168.32.89:2181,192.168.32.99:2181,192.168.32.101:2181,192.168.32.69:2181,192.168.32.79:2181,192.168.32.118:2181"
ZOOKEEPER_SERVERS = "192.168.50.11:2181,192.168.50.12:2181,192.168.50.13:2181,192.168.50.14:2181,192.168.50.15:2181"
TIMEOUT = 10.0
ZOO_ACL = [{'perms': 31, 'scheme': 'world', 'id': 'anyone'}]
AUTH = 'bfdrecommend:yijingzhijin987'

class ZKClient(object):
    def __init__(self, servers=ZOOKEEPER_SERVERS, timeout=TIMEOUT):
        self.connected = False
        self.conn_cv = threading.Condition( )
        self.handle = -1

        self.conn_cv.acquire()
        print("Connecting to %s" % (servers))
        self.handle = zookeeper.init(servers, self.connection_watcher, 30000)

        self.conn_cv.wait(timeout)
        self.conn_cv.release()

        if not self.connected:
            raise Exception("Unable to connect to %s" % (servers))

        print("Connected, handle is %d" % (self.handle))

    def connection_watcher(self, h, type, state, path):
        self.handle = h
        self.conn_cv.acquire()
        self.connected = True
        self.conn_cv.notifyAll()
        self.conn_cv.release()

    def close(self):
        zookeeper.close(self.handle)

    def exists(self, path):
	if zookeeper.exists(self.handle, path):
	    return True
	else:
	    return False

    def create(self, path, value):
	zookeeper.add_auth(self.handle, 'digest', AUTH, None)
	return zookeeper.create(self.handle, path, value, ZOO_ACL)

    def get(self, path):
        node_data =  zookeeper.get(self.handle, path)
        return node_data[0]

    def set(self, path, value):
	zookeeper.add_auth(self.handle, 'digest', AUTH, None)
	return zookeeper.set(self.handle, path, value)

    def delete(self, path):
	zookeeper.add_auth(self.handle, 'digest', AUTH, None)
	return zookeeper.delete(self.handle, path)

    def get_children(self, path, watcher=None):
        return zookeeper.get_children(self.handle, path, watcher)

    def get_acls(self, path):
        return zookeeper.get_acl(self.handle, path)

if __name__ == "__main__":
    zk = ZKClient()
    data = zk.get_children("/bre/common")
    print data
    #jsonobj = {"alg": {"read_timeout": 1000, "expiration_time": 20, "write_timeout": 1000}, "base": "base", "scenario": "scenario", "namespace": "ns1", "address": "192.168.32.89:2181,192.168.32.99:2181,192.168.32.101:2181,192.168.32.69:2181,192.168.32.79:2181,192.168.32.118:2181/Tripod", "rec": "rec"}    
    #zk.set("/bre/common/cache", json.dumps(jsonobj))
