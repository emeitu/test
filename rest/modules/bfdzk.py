# -*- coding=utf-8 -*-

import web
import json
import libzookeeper
import re
import time
import libpub as pub
from libpub import LOG
import uuid

urls = ['/bfdrest/bfdzk(/.+)']
zk = libzookeeper.ZKClient()


class handler:
    def GET(self,path):
        ''' /bfdrest/bfdzk/zkpath;
        '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        ret = {}
        try:
            data = zk.get(path)
            try:
                data = json.loads(data)
            except:
                pass
            ret['data'] = data
            ret['children'] = zk.get_children(path)
        except:
            pass
        if len(ret) == 0: ret = None
        return pub.callback(json.dumps(ret),myuuid)

