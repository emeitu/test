#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/opt/Ice-3.3/python/")
import traceback, Ice
import bfd.kafkaconsumerclient as kafka
import json
import time
import re
import os,fcntl
import pymongo
import MySQLdb as mdb
import urllib
BASE = os.path.dirname(os.path.abspath(__file__))

#bfdcloud/Locator:tcp -h m32p51 -p 7893:tcp -h m32p52 -p 7893
#default -h KafkaReplica1 -p 7074:default -h KafkaMaster -p 7074

class KafkaClient:
    def __init__(self):
        self.ic = None
        self.prx = None
        self.init()

    def init(self):
        list = ['--Ice.Override.ConnectTimeout=70',
        '--Ice.ThreadPool.Client.SizeMax=1000',
        '--Ice.ThreadPool.Client.StackSize=131072',
        '--Ice.ThreadPool.Server.SizeMax=1000',
        '--Ice.ThreadPool.Server.StackSize',
        '--Ice.MessageSizeMax=10240',
        '--IceGrid.InstanceName=KafkaChannel',
        '--Ice.Default.Locator=bfdcloud/Locator:default -h 192.168.50.16 -p 7893:default -h 192.168.50.17 -p 7893'
        ]
        try:
            self.ic = Ice.initialize(list)
            #base = self.ic.stringToProxy("M@BfdKafkaConsumerClient")
            base = self.ic.stringToProxy("M@KafkaConsumerProxy")
            self.prx = kafka.KafkaConsumerClientManagerPrx.checkedCast(base)
            if not self.prx:
                raise RuntimeError("Invalid proxy")
        except:
            traceback.print_exc()

    def setConsumeMethod(self,group,method):
        return self.prx.setConsumeMethod(group,method)

    def getUserID(self):
        return self.prx.getUserID()

    def getArray(self, topic, group, id, len):
        return self.prx.getArray(topic, group, id , len)

    def close(self, topic, group, id):
        return self.prx.close(topic,group,id)

def getData(topic,group,regex):
    kafka_client = KafkaClient()
    id = kafka_client.getUserID()
    msg_count=0
    msg_list=[]
    i = 0
    while i < 2:
        i+=1
        ret_array = []
        try:
            ret_array = kafka_client.getArray(topic,group,id,100)
            #print len(ret_array),ret_array
        except KeyboardInterrupt, e :
            print "KeyboardInterrupt, exit."
            break
        except Exception, e :
            LOG(e)
            traceback.print_exc()
            break
        for info in ret_array:
            #print "%d ret: %d, msg: %s" % (msg_count,info.ret,info.message)
            if info.ret == 1:
                msg_count+=1
                #print  "msg_count: ", msg_count
                if re.search(regex,info.message):
                    try:
                        #print "type: ",type(info.message)," info.msg: ", info.message
                        msg = json.loads(info.message)
                        msg_list.append(msg)
                    except:
                        pass
            else:
                return json.dumps(msg_list)
    kafka_client.close(topic,group,id)   #kafka_client.setConsumeMethod(group,1)
    return json.dumps(msg_list)



if __name__ == '__main__':
    print getData('DS.Input.All.Gka_5','test','.*')
