# -*- coding=utf-8 -*-

import web
import json
import libcache as cache
import re
import time

urls = ['/bfdrest/cache/(.+)']
GET_ret = 'value'
PUT_data = POST_data = 'value'
PUT_ret = POST_ret = DELETE_ret = 'True|False'

def get(key,pattern = None):
    if key.encode('utf8') == 'keys':
        if pattern:
            r = re.compile(pattern)
            keys = json.loads(cache.get('keys'))
            ret = {}
            for k in keys:
                if r.match(k):
                    ret[k] = keys[k]
            return json.dumps(sorted(ret.keys()))
        else:
            pass
            
    return cache.get(key)

def set(key,value):
    if key == 'keys':
        return False
    now = time.ctime()
    keystr = cache.get('keys')
    if keystr:
        keys = json.loads(keystr)
        keys[key] = now
    else:
       keys = {key:now} 
    if cache.set(key,value):
        return cache.set('keys',json.dumps(keys))
    else:
        return False

def delete(key,pattern=None):
    if key == 'keys' and not pattern:
        return False
    if key == 'keys' and pattern:
        r = re.compile(pattern)
        keys = json.loads(cache.get('keys'))
        klist = sorted(keys)
        for k in klist:
            if r.match(k):
                cache.delete(k)
                del keys[k]
        return cache.set('keys',json.dumps(keys))
        
    keys = json.loads(cache.get('keys'))
    if cache.delete(key):
        del keys[key]
        return cache.set('keys',json.dumps(keys))
    else:
        return False


class handler:
    def GET(self,key):
        ''' /bfdrest/cache/(key) for get key;
            /bfdrest/cache/keys for list all keys;
            /bfdrest/cache/keys?p=pattern for search key match pattern.
        '''
        data = web.input()
        p = None
        if 'p' in data:
            p = data['p']
        return get(key,p)

    def POST(self,key):
        ''' /bfdrest/cache/(key) '''
        value = web.data()
        return set(key,value)

    def PUT(self,key):
        ''' /bfdrest/cache/(key) '''
        value = web.data()
        return set(key,value)

    def DELETE(self,key):
        ''' /bfdrest/cache/(key) '''
        data = web.input()
        p = None
        if 'p' in data:
            p = data['p']
        return delete(key,p)
