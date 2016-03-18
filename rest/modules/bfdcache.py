# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web
import json
import libcache as cache
import re
import time
import ItemProfile_pb2
import RecBanner_pb2
import CategoryProfile_pb2
import UserProfile_pb2
import ImageFeature_pb2
import NewsProfile_pb2
import Scenario_pb2
import TagInfo_pb2
import GidChannelInfo_pb2
import Relation_pb2
import libpub as pub
from libpub import LOG
import uuid

urls = ['/bfdrest/bfdcache/(.+)/(.+)/(.+)/(.+)','/bfdrest/bfdcache/(.+)/(.+)/(.+)']
#urls = ['/bfdrest/bfdcache/([^/]+)/([^/]+)/(.+)']
GET_ret = 'value'

def proto2json(pm):
#    print pm
    rj = {}
    try:
        pm.ListFields()
    except:
        return pm
    for field in pm.ListFields():
        if field[0].type == field[0].TYPE_MESSAGE:
            if field[0].label == field[0].LABEL_REPEATED:
                rj[field[0].name] = []
                for msg in field[1]:
                    rj[field[0].name].append(proto2json(msg))
            else:
                rj[field[0].name] = proto2json(field[1])
        elif field[0].type == field[0].TYPE_STRING:
            if field[0].label == field[0].LABEL_REPEATED:
                rj[field[0].name] = []
                for msg in field[1]:
                    rj[field[0].name].append(msg.encode('utf-8'))
            else:
                rj[field[0].name] = field[1].encode('utf-8')
        elif field[0].label == field[0].LABEL_REPEATED:
            rj[field[0].name] = []
            for msg in field[1]:
                rj[field[0].name].append(proto2json(msg))
        else:
            rj[field[0].name] = field[1]
    print rj
    return rj

class handler:
    def GET(self,n,b,k,proto=None):
        ''' /bfdrest/bfdcache/namesapce/business/key for get key;
        '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        v = cache.get(k,n,b)
#        print '%s\t%s\t%s' % (n,b,k)
        if proto:
            if proto == 'DELETE':
                return pub.callback(json.dumps(cache.delete(k,n,b)),myuuid)
            if v == None or v == 'None':
                return pub.callback(json.dumps({}),myuuid)
            ib = eval("%s()"%proto)
            try:
                ib.ParseFromString(v)
            except Exception,e:
                return pub.callback(str(e),myuuid)
            return pub.callback(json.dumps(proto2json(ib)),myuuid)
        else:
            if v == None or v == 'None':
                return pub.callback(json.dumps(None),myuuid)
            return pub.callback(v,myuuid)

    def POST(self,n,b,k):
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.data()
        return pub.callback(cache.set(k,data,n,b),myuuid)
        

    def DELETE(self,n,b,k):
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        return pub.callback(cache.delete(k,n,b),myuuid)
