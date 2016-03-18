# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web
import json
import libhbase2 as libhbase
import re
import time
import ItemProfile_pb2
import RecBanner_pb2
import CategoryProfile_pb2
import UserProfile_pb2
import ImageFeature_pb2
import NewsProfile_pb2
import Scenario_pb2
import BrUserProfile_pb2
import CategoryProfile_pb2
import TagInfo_pb2
import libpub as pub
from libpub import LOG
import uuid

urls = ['/bfdrest/bfdhbase2/(.+)/(.+)/(.+)/(.+)/(.*)/(.+)','/bfdrest/bfdhbase2/(.+)/(.+)/(.+)/(.+)/(.*)/']
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
    def GET(self,host,table,key,family,column,proto=None):
        ''' /bfdrest/bfdhabase2/host/table/key/family/column(/proto) for get key;
        '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        v = libhbase.get_column(key,family,column,host,table)
        if not v:
            return pub.callback(v,myuuid)
        if proto:
            ib = eval("%s()"%proto)
            try:
                ib.ParseFromString(v)
            except Exception,e:
                return pub.callback(str(e),myuuid)
            return pub.callback(json.dumps(proto2json(ib)),myuuid)
        else:
            return pub.callback(v,myuuid)

