# -*- coding=utf-8 -*-

import web
import json
import libcache as cache
import libpub as pub
import libconf as conf
from libpub import LOG
import copy
import time
import cPickle
import google
import ItemProfile_pb2
import RecBanner_pb2
import md5
import goods
import uuid
#import logging

urls = ['/bfdrest/client/(.+)/banners/(.+)/logic_rule','/bfdrest/client/(.+)/banners/(.+)','/bfdrest/client/(.+)/banners']
GET_ret = {
    "name" : "",                    # 推荐栏名称
    "description" : "",             # 推荐栏描述
    "is_active" : True,             # 推荐栏是否开启
    "operation_rules" :             # 推荐栏逻辑规则
    [             
        ["operation_rule",None],    # [运营规则ID, 希望结果展示最多数量, null表示不做限制由服务端定]
        ["operation_rule",3],
        ["24",2],
        ["53",None],
    ],
    "position_rules":               # 推荐栏位置规则
    {
        "position_num" : ["goodsid"],    # 推荐栏位置（从0开始计数）：推荐商品库
        "0" : ["45223"]               # 如果没有指定商品库ID，不上传
    }
}

def ParseFromJson(cid,bid,json_banner):
    rb  = RecBanner_pb2.RecBanner()
    lr  = RecBanner_pb2.RecBanner.LogicRule()
    opr = RecBanner_pb2.RecBanner.LogicRule.OperationRule()
    pr  = RecBanner_pb2.RecBanner.LogicRule.PositionRule()
    uopr= RecBanner_pb2.OperationRule()
    gd  = RecBanner_pb2.Goods()

    bstr = cache.get('%s:RecBanner:%s'%(cid,bid))
    if bstr:
        try:
            rb.ParseFromString(bstr)
        except:
            print "parse from str failed"

    rb.banner_id    = bid
    rb.name         = json_banner["name"]
    rb.description  = json_banner["description"]
    if "is_active" in json_banner:
        rb.is_active    = json_banner["is_active"]
    else:
        rb.is_active = True
    rb.update_time  = int(time.time())
    
    if "operation_rules" in json_banner:
      for r_num in json_banner["operation_rules"]:
          opr.Clear()
          opr.operation_rule = r_num[0]
          if r_num[1]:
              opr.rec_num = r_num[1]
          else:
              opr.rec_num = -1
          opstr = cache.get('%s:OperationRule:%s'%(cid,r_num[0]))
          uopr.Clear()
          if opstr:
              try:
                uopr.ParseFromString(opstr)
                opr.user_level = uopr.user_level
              except:
                pass
          lr.operation_rules.add()
          lr.operation_rules[len(lr.operation_rules)-1].CopyFrom(opr)
    if "position_rules" in json_banner:
        for position in sorted(json_banner["position_rules"]):
            pr.Clear()
            pr.position = int(position)
            goodsid = json_banner["position_rules"][position]
            pr.goods_id.append(goodsid)
            goods_data = cache.get('%s:Goods:%s'%(cid,goodsid))
            if goods_data:
                try:
                    gd.ParseFromString(goods_data)
                    pr.user_level = gd.user_level
                except Exception, e:
            #        logging.error('except: %s', e)
                    pass
            lr.position_rules.add()
            lr.position_rules[len(lr.position_rules)-1].CopyFrom(pr)
    rb.logic_rule.CopyFrom(lr)
    return rb

class handler:
    def GET(self,cid,bid=None):
        ''' '/bfdrest/client/(cid)/banners','/bfdrest/client/(cid)/banners/(bid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        if bid == None:
            return pub.callback(json.dumps(GET_ret),myuuid)
        else:
            rstr = cache.get('%s:Banners:%s'%(cid,bid))
            ret = {}
            if rstr:
                ret = json.loads(rstr)
                ret["success"] = True
            else:
                ret["success"] = False
                ret["error_info"] = "no such banner id."
            return pub.callback(json.dumps(ret),myuuid)

    def POST(self,cid,bid):
        ''' '/bfdrest/client/(cid)/banners/(bid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.data()
        ret = {}
        rv = json.loads(data)
        rec_banner = ParseFromJson(cid,bid,rv)
        rlist = cache.get('%s:Banners:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        rlist[bid] = time.time()
        rstr = cache.set('%s:Banners:_all_'%(cid),json.dumps(rlist))
        rstr = cache.set('%s:RecBanner:%s'%(cid,bid),rec_banner.SerializeToString())
        rstr = cache.set('%s:Banners:%s'%(cid,bid),data)
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = False
            ret["error_info"] = "can't save banner info."
        return pub.callback(json.dumps(ret),myuuid)

    def PUT(self,cid,bid):
        ''' '/bfdrest/client/(cid)/banners/(bid)' '''
        return self.POST(cid,bid)

    def DELETE(self,cid,bid):
        ''' '/bfdrest/client/(cid)/banners/(bid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        rlist = cache.get('%s:Banners:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        if bid in rlist:
            del rlist[bid]
        cache.set('%s:Banners:_all_'%(cid),json.dumps(rlist))
        rstr = cache.delete('%s:Banners:%s'%(cid,bid))
        rstr = cache.delete('%s:RecBanner:%s'%(cid,bid))
        ret = {}
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = False
            ret["error_info"] = "can't delete banner info."
        return pub.callback(json.dumps(ret),myuuid)

