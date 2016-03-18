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

urls = ['/bfdrest/client/(.+)/operationrules/(.+)','/bfdrest/client/(.+)/operationrules']
GET_ret = {
    "name" : "",
    "description" : "",
    "condition" : [],
    "rec_ranges" : [
    ["_all_(全部商品)"],
    ["pid(品类范围)",["pid","一级类目"],["pid","二级类目"],["brand","品牌"]],
    ["brand(品牌范围)",["brand","品牌"],["pid","一级类目"],["pid","二级类目"]],
    ["goods(商品库)","商品库id"]
    ],
    "period" : {
      "start_time": {
        "day":"2013-1-1",
        "wday":"FF",
        "time":"11:00"
      },
      "end_time": {
        "day":"2013-10-1",
        "wday":"FF",
        "time":"21:00"
      },
      "time_type":"ymd"
    },
    "sort" : [
    ["pid(品类)",0], # (系统排序)
    ["brand(品牌)",1] # (同品牌优先)
    ]
}

def ParseFromJson(json_rule):
    op_rule = RecBanner_pb2.OperationRule()
    item_range = RecBanner_pb2.ItemRange()
    time_range = RecBanner_pb2.TimeRange()
    time_point = RecBanner_pb2.TimeRange.TimePoint()
    sort_rule = RecBanner_pb2.OperationRule.SortRule()

    op_rule.name = json_rule["name"]
    op_rule.description = json_rule["description"]
    if "user_level" in json_rule:
      op_rule.user_level = json_rule["user_level"]

    def parse_item_range(jir,has_ratio=False):
        ir = RecBanner_pb2.ItemRange()
        if len(jir) > 0:
            ir.type = jir[0]
            if has_ratio and len(jir) > 1:
                ir.ratio = int(jir[1])
                del jir[0:2]
            else:
                del jir[0]
            if ir.type == "goods":
                ir.goods_id = jir[0]
                del jir[0]
            if ir.type != "_all_":
                for pv in jir:
                    if len(pv) > 1 and pv[1] != "" and pv[1] != "_all_":
                        if pv[0] == 'price_less_than' or pv[0] == 'price_greater_than':
                            setattr(ir,pv[0],float(pv[1]))
                        else:
                            eval("ir.%s.append(pv[1])"%pv[0])
        return ir

    if len(json_rule["condition"]) > 0:
        op_rule.condition.CopyFrom(parse_item_range(json_rule["condition"]))

    for range in json_rule["rec_ranges"]:
        op_rule.rec_ranges.add()
        op_rule.rec_ranges[len(op_rule.rec_ranges)-1].CopyFrom(parse_item_range(range,True))

    for range in json_rule["filter_ranges"]:
        op_rule.filter_ranges.add()
        op_rule.filter_ranges[len(op_rule.filter_ranges)-1].CopyFrom(parse_item_range(range))

    time_range.type = json_rule["period"]["time_type"]
    time_point.day = json_rule["period"]["start_time"]["day"]
    time_point.time = json_rule["period"]["start_time"]["time"]
    time_point.wday = json_rule["period"]["start_time"]["wday"]
    time_range.start_time.CopyFrom(time_point)
    time_point.day = json_rule["period"]["end_time"]["day"]
    time_point.time = json_rule["period"]["end_time"]["time"]
    time_point.wday = json_rule["period"]["end_time"]["wday"]
    time_range.end_time.CopyFrom(time_point)
    op_rule.time_range.CopyFrom(time_range)

    if "sort" in json_rule:
        for l_sort in json_rule["sort"]:
            sort_rule.property = l_sort[0]
            sort_rule.type = int(l_sort[1])
            op_rule.sort_rules.add()
            op_rule.sort_rules[len(op_rule.sort_rules)-1].CopyFrom(sort_rule)

    return op_rule

class handler:
    def GET(self,cid,rid=None):
        ''' '/bfdrest/client/(cid)/operationrules','/bfdrest/client/(cid)/operationrules/(rid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        if rid == None:
            return pub.callback(json.dumps(GET_ret),myuuid)
        else:
            rstr = cache.get('%s:OperatorRules:%s'%(cid,rid))
            ret = {}
            if rstr:
                ret = json.loads(rstr)
                ret["success"] = True
            else:
                ret["success"] = False
                ret["error_info"] = "no such operation rule."
            return pub.callback(json.dumps(ret),myuuid)

    def POST(self,cid,rid):
        ''' '/bfdrest/client/(cid)/operationrules/(rid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.data()
        rv = json.loads(data)
        range_iids = {}
#range_iids = goods.generalize_ranges(cid,rv["rec_ranges"])
        riids = []
        for key in range_iids:
            riids.extend(range_iids[key])
        operation_rule = ParseFromJson(rv)
        operation_rule.operation_rule_id = rid
        rlist = cache.get('%s:OperatorRules:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        rlist[rid] = time.time()
        cache.set('%s:OperatorRules:_all_'%(cid),json.dumps(rlist))
        cache.set('%s:OperationRule:%s'%(cid,rid),operation_rule.SerializeToString())
        rstr = cache.set('%s:OperatorRules:%s'%(cid,rid),data)
        ret = {}
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = False
            ret["error_info"] = "can't save operation rule."
        return pub.callback(json.dumps(ret),myuuid)

    def PUT(self,cid,rid):
        ''' '/bfdrest/client/(cid)/operationrules/(rid)' '''
        return self.POST(cid,rid)

    def DELETE(self,cid,rid):
        ''' '/bfdrest/client/(cid)/operationrules/(rid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.input()
        jdata = data
        rstr = cache.delete('%s:OperationRule:%s'%(cid,rid))
        rstr = cache.delete('%s:OperatorRules:%s'%(cid,rid))
        rlist = cache.get('%s:OperatorRules:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        if rid in rlist:
            del rlist[rid]
        cache.delete('%s:OperatorRulesItems:%s'%(cid,rid))
        rstr = cache.set('%s:OperatorRules:_all_'%(cid),json.dumps(rlist))
        for p_bid in json.loads(jdata["banner_id"]):
            p_bid_str = cache.get("%s:RecBanner:%s"%(cid,p_bid))
            p_banner = RecBanner_pb2.RecBanner()
            if p_bid_str:
                p_banner.ParseFromString(p_bid_str)
                for i in xrange(len(p_banner.logic_rule.operation_rules)):
                    if p_banner.logic_rule.operation_rules[i].operation_rule == rid:
                        del p_banner.logic_rule.operation_rules[i]
                        break
            cache.set("%s:RecBanner:%s"%(cid,p_bid),p_banner.SerializeToString())
        ret = {}
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = False
            ret["error_info"] = "can't delete operation rule."
        return pub.callback(json.dumps(ret),myuuid)

