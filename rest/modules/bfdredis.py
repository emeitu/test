# -*- coding=utf-8 -*-

import web
import json
import libredis
import re
import time
import libpub as pub
from libpub import LOG
import uuid

urls = ['/bfdrest/bfdredis/(.+)/(.+)/(.+)/(.+)']
GET_ret = 'value'

def get(h,p,n,k):
    return libredis.get(h,p,n,k)


class handler:
    def GET(self,h,p,n,k):
        ''' /bfdrest/bfdredis/redis-server/port/db/key for get key;
        '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        return pub.callback(get(h,p,n,k),myuuid)

