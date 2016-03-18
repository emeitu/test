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

urls = ['/bfdrest/client/(.+)/ABtest/(.+)/(stop)','/bfdrest/client/(.+)/ABtest/(.+)','/bfdrest/client/(.+)/ABtest']
GET_ret = {
    "name":"",                             # ABtest方案名
    "description":"",                      # ABtest方案描述
    "traffic_ratio": 30,                   # ABtest使用流量百分比 0~100
    "start_time": {                        # ABtest起止时间,格式同运营规则生效时间
                           "day": "2013-1-1",
                           "wday": "FF",
                           "time": "11:00"
    },
    "end_time": {
        "day": "2013-10-1",
        "wday": "FF",
        "time": "21:00"
    },
    "time_type": "ymd",
    "banner_id": "832636",                # 绑定到的推荐栏
    "is_active": True,                    # "ABTest状态，是否开启",
    "condition" : [],                     # ABtest生效条件
    "test_a": {
      "rec_ranges" : [         # 推荐范围,前端保证范围不重复
        ["pid(品类范围)",10,["pid","二级类目"],["brand","品牌"]],
        ["brand(品牌范围)",20,["brand","品牌"],["pid","一级类目"],["pid","二级类目"]],
        ["goods(商品库)",30,"商品库id"]
      ],
      "filter_ranges" : [      # 非推荐范围,前端保证范围不重复
        ["pid(品类范围)",["pid","一级类目"],["pid","二级类目"],["brand","品牌"]],
        ["brand(品牌范围)",["brand","品牌"],["pid","一级类目"],["pid","二级类目"]],
        ["goods(商品库)","商品库id"]
      ],
      "sort" : [                     # 排序规则
        ["pid(品类)","0(系统排序)"],
        ["brand(品牌)","1(同品牌优先)"]
      ]
    },
    "test_b": {
      "rec_ranges" : [         # 推荐范围,前端保证范围不重复
        ["pid(品类范围)",10,["pid","二级类目"],["brand","品牌"]],
        ["brand(品牌范围)",20,["brand","品牌"],["pid","一级类目"],["pid","二级类目"]],
        ["goods(商品库)",30,"商品库id"]
      ],
      "filter_ranges" : [      # 非推荐范围,前端保证范围不重复
        ["pid(品类范围)",["pid","一级类目"],["pid","二级类目"],["brand","品牌"]],
        ["brand(品牌范围)",["brand","品牌"],["pid","一级类目"],["pid","二级类目"]],
        ["goods(商品库)","商品库id"]
      ],
      "sort" : [                     # 排序规则
        ["pid(品类)","0(系统排序)"],
        ["brand(品牌)","1(同品牌优先)"]
      ]
    }
}

def StopBannerABtest(cid,abid,jab):
    bannerstr = cache.get("%s:RecBanner:%s"%(cid,jab["banner_id"]))
    if not bannerstr:
        return False
    
    

def SetBannerABtest(cid,abid,jab,stop = False,delete = False):
    bannerstr = cache.get("%s:RecBanner:%s"%(cid,jab["banner_id"]))
    if not bannerstr:
        print "no banner_id"
        return False
    rb  = RecBanner_pb2.RecBanner()
    lr  = RecBanner_pb2.RecBanner.LogicRule()
    opr = RecBanner_pb2.RecBanner.LogicRule.OperationRule()
    pr  = RecBanner_pb2.RecBanner.LogicRule.PositionRule()
    abr = RecBanner_pb2.RecBanner.ABtestRule()
    ablr= RecBanner_pb2.RecBanner.ABtestRule.LogicRule()
    absr= RecBanner_pb2.RecBanner.ABtestRule.LogicRule.SortRule()
    tr  = RecBanner_pb2.TimeRange()
    tp  = RecBanner_pb2.TimeRange.TimePoint()
    ir  = RecBanner_pb2.ItemRange()
    try:
        rb.ParseFromString(bannerstr)
        if stop:
            abrstr = cache.get("%s:ABtestRule:%s"%(cid,abid))
            if not abrstr:
                print "no abtest_id"
                return False
            abr.ParseFromString(abrstr)
            abr.is_active = False
            cache.set("%s:ABtestRule:%s"%(cid,abid),abr.SerializeToString())
            for i in xrange(len(rb.abtest_rules)):
                if abid == rb.abtest_rules[i].abtest_id:
                    rb.abtest_rules[i].is_active = False
                    break
            rb.update_time = int(time.time())
            return cache.set("%s:RecBanner:%s"%(cid,jab["banner_id"]),rb.SerializeToString())
        if delete:
            for i in xrange(len(rb.abtest_rules)):
                if abid == rb.abtest_rules[i].abtest_id:
                    del(rb.abtest_rules[i])
                    break
            rb.update_time = int(time.time())
            return cache.set("%s:RecBanner:%s"%(cid,jab["banner_id"]),rb.SerializeToString())
        abr.abtest_id = abid
        abr.name = jab["name"]
        abr.description = jab["description"]
        abr.traffic_ratio = jab["traffic_ratio"]
        abr.is_active = jab["is_active"]
        abr.banner_id = jab["banner_id"]
        if "user_level" in jab:
            abr.user_level = jab["user_level"]

        tr.type = jab["time_type"]
        tp.day  = jab["start_time"]["day"]
        tp.time = jab["start_time"]["time"]
        tp.wday = jab["start_time"]["wday"]
        tr.start_time.CopyFrom(tp)
        tp.day  = jab["end_time"]["day"]
        tp.time = jab["end_time"]["time"]
        tp.wday = jab["end_time"]["wday"]
        tr.end_time.CopyFrom(tp)
        abr.time_range.CopyFrom(tr)

        def parse_item_range(jir,has_ratio=False):
            ir.Clear()
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
                        if pv[0] == 'price_less_than' or pv[0] == 'price_greater_than':
                            setattr(ir,pv[0],float(pv[1]))
                        else:
                            eval("ir.%s.append(pv[1])"%pv[0])
            return ir
        if len(jab["condition"]) > 0:
            abr.condition.CopyFrom(parse_item_range(jab["condition"]))

        def parse_logic_rule(jlr):
            ablr.Clear()
            if "rec_ranges" in jlr:
                for jir in jlr["rec_ranges"]:
                    ablr.rec_ranges.add()
                    ablr.rec_ranges[len(ablr.rec_ranges)-1].CopyFrom(parse_item_range(jir,True))
            if "filter_ranges" in jlr:
                for jir in jlr["filter_ranges"]:
                    ablr.filter_ranges.add()
                    ablr.filter_ranges[len(ablr.filter_ranges)-1].CopyFrom(parse_item_range(jir))
            if "sort" in jlr:
                for jsr in jlr["sort"]:
                    absr.Clear()
                    absr.property = jsr[0]
                    absr.type = int(jsr[1])
                    ablr.sort_rules.add()
                    ablr.sort_rules[len(ablr.sort_rules)-1].CopyFrom(absr)
            return ablr
        abr.logic_rules.add()
        abr.logic_rules.add()
        abr.logic_rules[0].CopyFrom(parse_logic_rule(jab["test_a"]))
        abr.logic_rules[1].CopyFrom(parse_logic_rule(jab["test_b"]))

        new_abtest = True
        for i in xrange(len(rb.abtest_rules)):
            if abid == rb.abtest_rules[i].abtest_id:
                rb.abtest_rules[i].Clear()
                rb.abtest_rules[i].CopyFrom(abr)
                new_abtest = False
                break
        if new_abtest:
            rb.abtest_rules.add()
            rb.abtest_rules[len(rb.abtest_rules)-1].CopyFrom(abr)
        rb.update_time = int(time.time())
        rstr = cache.set('%s:ABtestRule:%s'%(cid,abid),abr.SerializeToString())
        return cache.set("%s:RecBanner:%s"%(cid,jab["banner_id"]),rb.SerializeToString())
    except Exception,e:
        print "err: " + str(e)
        return False
    

class handler:
    def GET(self,cid,abid=None):
        ''' '/bfdrest/client/(cid)/ABtest','/bfdrest/client/(cid)/ABtest/(ABid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        if abid == None:
            return pub.callback(json.dumps(GET_ret),myuuid)
        else:
            rstr = cache.get('%s:ABtest:%s'%(cid,abid))
            if abid == "_all_":
                return rstr
            ret = {}
            if rstr:
                ret = json.loads(rstr)
                ret["success"] = True
            else:
                ret["success"] = False
                ret["error_info"] = "no such ABtest id."
            return pub.callback(json.dumps(ret),myuuid)

    def POST(self,cid,abid,method=None):
        ''' '/bfdrest/client/(cid)/ABtest/(abid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        stop = False
        if method == "stop":
            stop = True
        data = web.data()
        ret = {}
        rv = json.loads(data)
        if not SetBannerABtest(cid,abid,rv,stop):
            ret["success"] = False
            ret["error_info"] = "can't save banner abtest."
            return pub.callback(json.dumps(ret),myuuid)
        rlist = cache.get('%s:ABtest:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        rlist[abid] = time.time()
        rstr = cache.set('%s:ABtest:_all_'%(cid),json.dumps(rlist))
        rstr = cache.set('%s:ABtest:%s'%(cid,abid),data)
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = False
            ret["error_info"] = "can't save abtest rule."
        return pub.callback(json.dumps(ret),myuuid)

    def PUT(self,cid,abid):
        ''' '/bfdrest/client/(cid)/ABtest/(abid)' '''
        return self.POST(cid,abid)

    def DELETE(self,cid,abid):
        ''' '/bfdrest/client/(cid)/ABtest/(abid)' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.input()
        rv = data
        ret = {}
        if not SetBannerABtest(cid,abid,rv,False,True):
            ret["success"] = False
            ret["error_info"] = "can't delete banner abtest."
            return pub.callback(json.dumps(ret),myuuid)
        rlist = cache.get('%s:ABtest:_all_'%cid)
        if rlist:
            rlist = json.loads(rlist)
        else:
            rlist = {}
        if abid in rlist:
            del rlist[abid]
        rstr = cache.set('%s:ABtest:_all_'%(cid),json.dumps(rlist))
        rstr = cache.delete('%s:ABtest:%s'%(cid,abid))
        rstr = cache.delete('%s:ABtestRule:%s'%(cid,abid))
        if rstr:
            ret["success"] = True
        else:
            ret["success"] = True
            ret["error_info"] = "can't delete abtest rule."
        return pub.callback(json.dumps(ret),myuuid)

