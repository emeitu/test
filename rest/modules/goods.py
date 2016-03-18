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
import category
import urllib
import uuid

quote = urllib.quote

urls = ['/bfdrest/client/(.+)/goods/(.+)/(random)/(.+)','/bfdrest/client/(.+)/goods/(.+)/(items)','/bfdrest/client/(.+)/goods/(.+)','/bfdrest/client/(.+)/goods']

PUT_data = POST_data ={
    "name": "goods name",
    "description": "goods description",
    "is_active": True,
    "items": [
        {
            "item_id": "",
            "item_title": "",
            "image_url": ""
        }
    ],
    "ranges": [
        [
            ["brd","abc"],
            ["cat","1"],
            ["cat","11"]
        ],
        [
            ["cat","1"],
            ["cat","11"],
            ["brd","abc"]
        ]
    ]
}

PUT_ret = POST_ret ={
    "success": True,
    "faild_items": {
        "item_id": "msg"
    },
    "faild_ranges":{
        "range": "msg"
    },
    "error_info": "item error"
}

GET_ret = {
'/bfdrest/client/(.+)/goods':
{
    "success": True,
    "error_info": "",
    "must_fields": {
        "item_id": ["iid","string"],
        "item_name": ["name","string"],
        "price": ["price","double"],
        "other": ["proto_field","type"]
    },
    "optional_fields": {
        "author": ["author","string"],
        "color": ["color","string"],
        "other": ["proto_field","type"]
    }
},
'/bfdrest/client/(cid)/goods/(goodsid)':
{
    "success": True,
    "error_info": "",
    "name": "goods name",
    "description": "goods description",
    "is_active": True,
    "items": [
        {
            "item_id": "",
            "item_title": "",
            "image_url": ""
        }
    ],
    "ranges": [
        [
            ["brd","abc"],
            ["cat","1"],
            ["cat","11"]
        ],
        [
            ["cat","1"],
            ["cat","11"],
            ["brd","abc"]
        ]
    ]
}
}

goods_fields = {'succees':True,'error_info':'','must_fields':{},'optional_fields':{}}
ibtmp = ItemProfile_pb2.ItemBase()
fdtmp = google.protobuf.descriptor.FieldDescriptor
for fd in ibtmp.DESCRIPTOR.fields:
    fd_name = fd.name
    fd_type = pub.proto_field_type[fd.type]
    if fd.label == fdtmp.LABEL_REQUIRED:
        goods_fields['must_fields'][fd_name] = [fd.name,fd_type]
    else:
        goods_fields['optional_fields'][fd_name] = [fd.name,fd_type]

goods_fields = {
"optional_fields": [
],
"succees": True,
"must_fields": [
["商品id",
"iid",
"string"
],
["商品名称",
"name",
"string"
],
["商品详情页链接地址",
"url",
"url"
],
["商品缩略图链接地址",
"simg",
"url"
],
["商品市场价",
"mktp",
"double"
],
["商品商城价",
"prc",
"double"
]
],
"error_info": ""
}

goods_fields_conf = {
    "Csanfu" : {
        "optional_fields": [],
        "succees": True,
        "must_fields": [
            ["商品id",
            "iid",
            "string"
            ]
        ],
        "error_info": ""
    }
}

type_define = {
"int32" : "^-?[1-9]\d{0,8}$",
"int64" : "^-?[1-9]\d{0,19}$",
"double" : "^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0|[1-9]\d{0,19})$",
"string" : "^.{0,1000}$",
"url" : "^[a-zA-z]+:\/\/[^\s]*$",
"list" : "^([^|]+\|){0,}[^|]*$",
"json" : r'^("(\\.|[^"\\\n\r])*?"|[,:{}\[\]0-9.\-+Eaeflnr-u \r\t])+?$'
}

DELETE_ret = {
    "success": True,
    "error_info": "",
}

client_conf = conf.get_all_conf()
#property_tree = cPickle.load(open('./data/Czouxiu.ptree.pkl','rb'))
client_property_tree = category.client_property_tree

def is_type(data,template):
    return type(data) == type(template)

#solr_url = 'http://192.168.32.163:9090/solr/collection1/select?&wt=json&indent=true&rows=500'
#update_item_url = 'http://192.168.3.150:19000/2.0/UpdateItem.do?ignore_domain=1&store=1'
#delete_item_url = 'http://test.ds.api.baifendian.com/2.0/RmItem.do?ignore_domain=1&store=1'
update_item_url = 'http://ds.api.baifendian.com/2.0/UpdateItem.do?ignore_domain=1&store=1'
delete_item_url = 'http://ds.api.baifendian.com/2.0/RmItem.do?ignore_domain=1&store=1'
solr_url = 'http://192.168.61.35:9090/solr/collection1/select?&wt=json&indent=true&rows=500'
def rm_goods_solr(cid,gsid,items=[]):
    ret = cache.get("%s:GoodsItems:%s"%(cid,gsid))
    j = []
    if ret:
        j = json.loads(ret)
    new_items = set()
    for item in items:
        new_items.add(item['iid'])
    for iid in j:
        if iid in new_items:
            continue
        cache_key = "%s:ItemBase:%s" % (cid,iid)
        cache_str = cache.get(cache_key,'ns1','item')
        if cache_str:
            ib = ItemProfile_pb2.ItemBase()
            ib.ParseFromString(cache_str)
            gsids = ib.goods
            gsid_set = set()
            for old_gsid in gsids:
                if old_gsid != gsid:
                    gsid_set.add(old_gsid)
            if len(gsid_set) == 0 and not ib.is_verified:
                del_url = '%s&cid=%s&iid=%s'%(delete_item_url,cid,iid)
                print "delete item, id: %s" % del_url
                urllib.urlopen(del_url)
            else:
                update_url = '%s&cid=%s&iid=%s&gsid=%s'%(update_item_url,cid,iid,'|'.join(gsid_set))
                print "update item goods id: %s" % update_url
                urllib.urlopen(update_url)
    

def generalize_items(client,gsid,items):
    iids = []
    info = {'success':True,'error_info':'','faild_items':{}}
    for item_info in items:
        if 'iid' not in item_info:
            info['success'] = False
            info['error_info'] += "item error, some item have no iid. "
            continue
        iid = item_info['iid']
        add_item_url = 'http://ds.api.baifendian.com/2.0/AddItem.do?ignore_domain=1&store=1&cid=%s&iid=%s' % (quote(client),quote(iid))
        for key in item_info:
            try:
                add_item_url += '&%s=%s' % (key,urllib.quote(item_info[key].encode('utf-8')))
                pass
            except Exception,e:
                info['success'] = False
                info['error_info'] += "item info error."
                info['faild_items'][iid] = key + str(e)
        cache_key = "%s:ItemBase:%s" % (client,iid)
        cache_str = cache.get(cache_key,'ns1','item')
        if not cache_str:
            try:
                add_item_url += "&gsid=%s" % quote(gsid)
                print add_item_url
                add_ret = urllib.urlopen(add_item_url)
                ret = json.loads(add_ret.readline())
                print ret
                if ret[0] == 0:
                    iids.append(iid)
                else:
                    info['success'] = False
                    info['error_info'] += "AddItem error."
                    info['faild_items'][iid] = json.dumps(ret)
            except Exception,e:
                info['success'] = False
                info['error_info'] += "AddItem error."
                info['faild_items'][iid] = str(e)
        else:
            add_item_url = 'http://ds.api.baifendian.com/2.0/UpdateItem.do?ignore_domain=1&store=1&cid=%s&iid=%s' % (quote(client),quote(iid))
            try:
                ib = ItemProfile_pb2.ItemBase()
                ib.ParseFromString(cache_str)
                ibgoods_set = set()
                for gsid_ in ib.goods:
                    ibgoods_set.add(gsid_)
                ibgoods_set.add(gsid)
                if not ib.is_verified:
                    for key in item_info:
                        try:
                            add_item_url += '&%s=%s' % (key,urllib.quote(item_info[key].encode('utf-8')))
                            pass
                        except Exception,e:
                            info['success'] = False
                            info['error_info'] += "item info error."
                            info['faild_items'][iid] = key + str(e)
                add_item_url += "&gsid=%s" % quote('|'.join(ibgoods_set))
                print add_item_url
                add_ret = urllib.urlopen(add_item_url)
                ret = json.loads(add_ret.readline())
                print ret
                if ret[0] == 0:
                    iids.append(iid)
                else:
                    info['success'] = False
                    info['error_info'] += "AddItem error."
                    info['faild_items'][iid] = json.dumps(ret)
            except Exception,e:
                info['success'] = False
                info['error_info'] += "AddItem error."
                info['faild_items'][iid] = str(e)
    return iids,info
                

def generalize_ranges(client,ranges):
    range_iids = {}
    if client not in client_conf:
        main_property = client_conf["Cdemo"]['main_property']
        all_properties = client_conf["Cdemo"]["properties"]
    else:
        main_property = client_conf[client]['main_property']
        all_properties = client_conf[client]["properties"]
    print main_property
    # find main property path and other property
    print ranges
    if client not in client_property_tree:
        client_property_tree[client] = cPickle.load(open('./data/%s.ptree.pkl'%client,'rb'))
    property_tree = client_property_tree[client]
    for range in ranges:
        iids = []
        main_path = []
        property_path = []
        print range
        if len(range) > 0:
            tag = range[0]
            if tag in all_properties:
                del range[0]
            elif tag == "_all_":
                del range[0]
                continue
            elif tag == "goods":
                goodsid = range[1]
                gstr = cache.get("%s:Goods:%s"%(client,goodsid))
                if gstr:
                    gv = json.loads(gstr)
                    if "keys" in gv:
                        for key in gv["keys"]:
                            rstr = cache.get("%s:GoodsItems:%s"%(client,key))
                            if rstr:
                                iids.extend(json.loads(rstr))
                    rstr = cache.get("%s:GoodsItems:%s"%(client,goodsid))
                    if rstr:
                        iids.extend(json.loads(rstr))
                range_iids[goodsid] = iids
                continue
        for pv in range:
            property = pv[0]
            value = pv[1]
            if value == "_all_":
                continue
            if property == main_property:
                main_path.append(value)
            else:
                property_path.append(pv)
        print ("main_path",main_path)
        print ("property_apth",property_path)
        cur_tree = property_tree
        find_path = True
        for path_node in main_path:
            if path_node in cur_tree['nodes']:
                cur_tree = cur_tree['nodes'][path_node]
            else:
                find_path = False
        if not find_path:
            continue
        def add_iids(tree_node):
            for id in tree_node['items']:
                id_in_range = True
                for pv in property_path:
                    property = pv[0]
                    value = pv[1]
#                    print "property:%s" % str(pv)
                    if property not in tree_node['items'][id] or value not in tree_node['items'][id][property]:
                        id_in_range = False
                if id_in_range:
                    iids.append(id)
            for next_node in tree_node['nodes']:
                add_iids(tree_node['nodes'][next_node])
        add_iids(cur_tree)
        path_key = md5.new(json.dumps([main_path,property_path])).hexdigest()
        range_iids[path_key] = iids
    return range_iids

def remove_goods_relation(cid,goods_id,jdata):
    for p_bid in json.loads(jdata["banner_id"]):
        p_bid_str = cache.get("%s:RecBanner:%s"%(cid,p_bid))
        p_banner = RecBanner_pb2.RecBanner()
        if p_bid_str:
            p_banner.ParseFromString(p_bid_str)
            n = 0
            for i in xrange(len(p_banner.logic_rule.position_rules)):
                for j in xrange(len(p_banner.logic_rule.position_rules[i-n].goods_id)):
                    if p_banner.logic_rule.position_rules[i-n].goods_id[j] == goods_id:
                        del p_banner.logic_rule.position_rules[i-n].goods_id[j]
                        break
                if len(p_banner.logic_rule.position_rules[i-n].goods_id) == 0:
                    del p_banner.logic_rule.position_rules[i-n]
                    n += 1
            cache.set("%s:RecBanner:%s"%(cid,p_bid),p_banner.SerializeToString())
    for ab_id in json.loads(jdata["abtest_id"]):
        ab_str = cache.get('%s:ABtestRule:%s'%(cid,ab_id))
        p_ab = RecBanner_pb2.RecBanner.ABtestRule()
        if ab_str:
            p_ab.ParseFromString(ab_str)
            for logic_rule in p_ab.logic_rules:
                for i in xrange(len(logic_rule.rec_ranges)):
                    if logic_rule.rec_ranges[i].type == "goods" and logic_rule.rec_ranges[i].goods_id == goods_id:
                        del logic_rule.rec_ranges[i]
                        break
                for i in xrange(len(logic_rule.filter_ranges)):
                    if logic_rule.filter_ranges[i].type == "goods" and logic_rule.filter_ranges[i].goods_id == goods_id:
                        del logic_rule.filter_ranges[i]
                        break
            cache.set('%s:ABtestRule:%s'%(cid,ab_id),p_ab.SerializeToString())
            p_bid = p_ab.banner_id
            p_bid_str = cache.get("%s:RecBanner:%s"%(cid,p_bid))
            p_banner = RecBanner_pb2.RecBanner()
            if p_bid_str:
                p_banner.ParseFromString(p_bid_str)
                for ab in p_banner.abtest_rules:
                    if ab.abtest_id == ab_id:
                        ab.Clear()
                        ab.CopyFrom(p_ab)
                        break
                cache.set("%s:RecBanner:%s"%(cid,p_bid),p_banner.SerializeToString())
    for op_id in json.loads(jdata["operation_id"]):
        op_str = cache.get('%s:OperationRule:%s'%(cid,op_id))
        p_op = RecBanner_pb2.OperationRule()
        if op_str:
            p_op.ParseFromString(op_str)
            for i in xrange(len(p_op.rec_ranges)):
                if p_op.rec_ranges[i].type == "goods" and p_op.rec_ranges[i].goods_id == goods_id:
                    del p_op.rec_ranges[i]
                    break
            for i in xrange(len(p_op.filter_ranges)):
                if p_op.filter_ranges[i].type == "goods" and p_op.filter_ranges[i].goods_id == goods_id:
                    del p_op.rec_ranges[i]
                    break
            cache.set('%s:OperationRule:%s'%(cid,op_id),p_op.SerializeToString())
        
class handler:
    def GET(self,cid,goodsid=None,range=None):
        ''' /bfdrest/client/(cid)/goods/(goodsid)/(items) '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        if goodsid == None:
            if cid in goods_fields_conf:
                return pub.callback(json.dumps(goods_fields_conf[cid]),myuuid)
            return pub.callback(json.dumps(goods_fields),myuuid)
        elif goodsid == "type":
            return pub.callback(json.dumps(type_define),myuuid)
        else:
            gv = cache.get('%s:Goods:%s'%(cid,goodsid))
            if gv:
                ret = json.loads(gv)
                ret['success'] = True
                if range == None:
                    if 'keys' in ret:
                        del ret['keys']
                        pass
                    return pub.callback(json.dumps(ret),myuuid)
                else:
                    iids = []
                    # 获取范围的item
                    for key in [goodsid]:
                        ids_str = cache.get('%s:GoodsItems:%s'%(cid,key))
                        if ids_str:
                            iids.extend(json.loads(ids_str))
                    return pub.callback(json.dumps(iids),myuuid)

            else:
                ret = {}
                ret['success'] = False
                ret['error_info'] = 'no such goods id.'
                return pub.callback(json.dumps(ret),myuuid)

    def POST(self,cid,goodsid):
        ''' /bfdrest/client/(cid)/goods/(goodsid) '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        value = web.data()
        put_value = {}
        ret = {}
        data = {}
        pgs = RecBanner_pb2.Goods()
        g_str = cache.get('%s:Goods:%s'%(cid,goodsid))
        if g_str:
            pgs.ParseFromString(g_str)
        pgs.goods_id = goodsid
        try:
            put_value = json.loads(value)
        except Exception,e:
            ret["success"] = False
            ret["error_info"] = "wrong json format: %s" % str(e)
            return pub.callback(json.dumps(ret),myuuid)
        if put_value.has_key('name'):
            data['name'] = put_value['name']
            pgs.name = put_value['name']
        else:
            data['name'] = ""
        if put_value.has_key('description'):
            data['description'] = put_value['description']
            pgs.description = put_value['description']
        else:
            data['description'] = ""
        if "user_level" in put_value:
            data["user_level"] = put_value["user_level"]
            pgs.user_level = put_value["user_level"]
        pgs.is_ranges = False
        if put_value.has_key('items') and len(put_value['items']) > 0:
            ret["success"] = True
            # save goods
            data['items'] = put_value['items']
            # 待添加具体功能,更新ItemBase,更新商品库商品
            rm_goods_solr(cid,goodsid,data['items'])
            iids,info = generalize_items(cid,goodsid,data['items'])
            data['keys'] = [goodsid]
            del data['items']
            goods_list = cache.get('%s:Goods:_all_'%cid)
            if goods_list:
                goods_list = json.loads(goods_list)
            else:
                goods_list = {}
            goods_list[goodsid] = time.time()
            cache.set('%s:Goods:_all_'%cid,json.dumps(goods_list))
            cache.set('%s:GoodsItems:%s'%(cid,goodsid),json.dumps(iids))
            cache.set('%s:Goods:%s'%(cid,goodsid),pgs.SerializeToString())
            return pub.callback(json.dumps(info),myuuid)
        elif put_value.has_key('ranges') and len(put_value['ranges']) > 0:
            pgs.is_ranges = True
            for i in xrange(len(pgs.ranges)):
                del pgs.ranges[0]
            ret["success"] = True
            # save goods
            data['ranges'] = put_value['ranges']
            
            def parse_item_range(jir,has_ratio=False):
                ir = RecBanner_pb2.ItemRange()
                if len(jir) > 0:
                    ir.type = jir[0][0]
                    for pv in jir:
                        if len(pv) > 1 and pv[1] != "_all_":
                            eval("ir.%s.append(pv[1])"%pv[0])
                return ir
            for range in put_value['ranges']:
                pgs.ranges.add()
                pgs.ranges[len(pgs.ranges)-1].CopyFrom(parse_item_range(range))

            #rm_goods_solr(cid,goodsid)
            range_iids = generalize_ranges(cid,data['ranges'])
            data["keys"] = range_iids.keys()
            iids = []
            for key in range_iids:
                iids.extend(range_iids[key])
            goods_list = cache.get('%s:Goods:_all_'%cid)
            if goods_list:
                goods_list = json.loads(goods_list)
            else:
                goods_list = {}
            goods_list[goodsid] = time.time()
            cache.set('%s:Goods:_all_'%cid,json.dumps(goods_list))
            cache.set('%s:GoodsItems:%s'%(cid,goodsid),json.dumps(iids))
            cache.set('%s:Goods:%s'%(cid,goodsid),pgs.SerializeToString())
            # 待添加具体功能,更新商品库商品
            return pub.callback(json.dumps(ret),myuuid)
        else:
            ret["success"] = True
            cache.set('%s:Goods:%s'%(cid,goodsid),pgs.SerializeToString())
            return pub.callback(json.dumps(ret),myuuid)

    def PUT(self,cid,goodsid):
        ''' /bfdrest/client/(cid)/goods/(goodsid) '''
        return self.POST(cid,goodsid)

    def DELETE(self,cid,goodsid):
        ''' /bfdrest/client/(cid)/goods/(goodsid) '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        data = web.input()
        jdata = data
        ret = {}
        g_str = cache.get('%s:Goods:%s'%(cid,goodsid))
        pgs = RecBanner_pb2.Goods()
        if g_str:
            pgs.ParseFromString(g_str)
            if not pgs.is_ranges:
                rm_goods_solr(cid,goodsid)
        cache.delete('%s:Goods:%s'%(cid,goodsid))
        remove_goods_relation(cid,goodsid,jdata)
        goods_list = cache.get('%s:Goods:_all_'%cid)
        if goods_list:
            goods_list = json.loads(goods_list)
        else:
            goods_list = {}
        if goodsid in goods_list:
            del goods_list[goodsid]
            cache.set('%s:Goods:_all_'%cid,json.dumps(goods_list))
        ret['success'] = True
        return pub.callback(json.dumps(ret),myuuid)

