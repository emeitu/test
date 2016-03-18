# -*- coding=utf-8 -*-

# server addresses
#ZK = "192.168.32.89:2181,192.168.32.99:2181,192.168.32.101:2181,192.168.32.69:2181,192.168.32.79:2181,192.168.32.118:2181"
#ZK = "bfd5-rec1:2181,bfd5-rec2:2181,bfd5-rec3:2181,bfd5-rec4:2181,bfd5-ice1:2181,bfd5-ice2:2181"
ZK = "192.168.50.11:2181,192.168.50.12:2181,192.168.50.13:2181,192.168.50.14:2181,192.168.50.15:2181"
TRIPOD_ADDR = "/".join((ZK, "Tripod"))
import PyBfdCache
import libredis as r

bfdcache = {}

def get(key,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    return PyBfdCache.get(bfdcache[(n,b)],key.encode('utf8'))

def mget(keys,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    return PyBfdCache.mget(bfdcache[(n,b)],keys.encode('utf8'))

def set(key,value,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    #r.set('192.168.49.23',6380,15,'%s_%s_%s'%(n,b,key),value)
    return PyBfdCache.set(bfdcache[(n,b)],key,value,0)

def mset(key_values,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    return PyBfdCache.mset(bfdcache[(n,b)],key_values)

def delete(key,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    return PyBfdCache.delete(bfdcache[(n,b)],key)

def mdelete(keys,n='ns1',b='breconf'):
    if (n,b) not in bfdcache:
        bfdcache[(n,b)] = PyBfdCache.newClient(TRIPOD_ADDR,n,b)
    return PyBfdCache.mdelete(bfdcache[(n,b)],keys)
