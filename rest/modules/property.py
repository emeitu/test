# -*- coding=utf-8 -*-

import web
import json
import libpub as pub

urls = ['/bfdrest/client/(.+)/property']

PUT_data = POST_data = {"property":"value","property_repeat":[]}

PUT_ret = POST_ret = 'True|False'

GET_ret = {"property":{"main_property":{"tree_property":"name"},"properties":{"index_property":"name"}}}

DELETE_ret = 'True|False'

"""
def delete_item(cid,iid):
    iidstr = cache.get('%s:index:iid:%s'%(cid,iid))
    if iidstr:
        obj = json.loads(iidstr)
        cate = ""
        for i in range(len(obj['cat'])):
            cate = cate + ':' + obj['cat'][i]
            catestr = cache.get('%s:index:cat%s'%(cid,cate))
            cateobj = json.loads(catestr)
            for property in obj:
                if property == 'cat':
                    if len(obj['cat']) > i+1:
                        if obj['cat'][i+1] in cateobj['cat']:
                            cateobj['cat'][(obj['cat'][i+1])] -= 1
                elif property == 'iid':
                    if i == len(obj['cat'])-1:
                        del cateobj['iid'][obj['iid']]
                elif isinstance(obj[property],list):
                    for p in obj[property]:
                        if p in cateobj[property]:
                            cateobj[property][p] -= 1
                else:
                    if obj[property] in cateobj[property]:
                        cateobj[property][obj[property]] -= 1
            properties = cateobj.keys()
            for property in properties:
                ps = cateobj[property].keys()
                for p in ps:
                    if cateobj[property][p] == 0:
                        del cateobj[property][p]
                if len(cateobj[property]) == 0:
                    del cateobj[property]
            if catestr != json.dumps(cateobj):
                if len(cateobj) > 0:
                    cache.set('%s:index:cat%s'%(cid,cate),json.dumps(cateobj))
                else:
                    cache.delete('%s:index:cat%s'%(cid,cate))
        for property in obj:
            if property == 'cat' or property == 'iid':
                continue
            if isinstance(obj[property],list):
                for p in obj[property]:
                    pstr = cache.get('%s:index:%s:%s'%(cid,property,p))
                    pobj = json.loads(pstr)
                    del pobj[obj['iid']]
                    if pstr != json.dumps(pobj):
                        if len(pobj) > 0:
                            cache.set('%s:index:%s:%s'%(cid,property,p),json.dumps(pobj))
                        else:
                            cache.delete('%s:index:%s:%s'%(cid,property,p))
            else:
                p = obj[property]
                pstr = cache.get('%s:index:%s:%s'%(cid,property,p))
                pobj[obj['iid']]
                if pstr != json.dumps(pobj):
                    if len(pobj) > 0:
                        cache.set('%s:index:%s:%s'%(cid,property,p),json.dumps(pobj))
                    else:
                        cache.delete('%s:index:%s:%s'%(cid,property,p))
        cache.delete('%s:index:iid:%s'%(cid,iid))
    return True
"""

class handler:
    def GET(self,cid):
        '''  
            /bfdrest/client/(cid)/property like /bfdrest/client/Czouxiu/property
        '''
        ret = {
            "success"   : True,
            "error_info"    : "",
            "main_property" : {"pid":"分类"},
            "properties"    : {"pid":"分类","brand":"品牌"}
        }
#data = web.input()
#callback = ""
#        if 'callback' in data:
#            callback = data['callback']
        if cid == "Czouxiu" or cid == "Ctest_ifec":
            return pub.callback(json.dumps(ret))
        else:
            ret = {}
            ret["success"] = False
            ret["error_info"] = "No such clent. client: " + cid
            return pub.callback(json.dumps(ret))
"""
    def POST(self,cid):
        ''' /bfdrest/client/(cid)/property '''
        value = web.data()
        value_error = '{"stat":false,"info":"Wrong json data","format":{"property":"value","property_repeat":[]}}'
        try:
            v = json.loads(value)
        except:
            return value_error

        if 'iid' not in v:
            return '{"stat":false,"info":"no iid"}'
        if 'cat' not in v:
            v['cat'] = ['_all_']
        else:
            v['cat'].insert(0,'_all_')
        # 更新商品索引前删除旧索引,无变化直接返回
        iidstr = cache.get('%s:index:iid:%s'%(cid,v['iid']))
        if iidstr == json.dumps(v):
            return True
        elif iidstr:
            delete_item(cid,v['iid'])
        # 更新商品索引
        cache.set('%s:index:iid:%s'%(cid,v['iid']),json.dumps(v))
        # 更新类目索引
        cate = ""
        for i in range(len(v['cat'])):
            cate = cate + ':' + v['cat'][i]
            catestr = cache.get('%s:index:cat%s'%(cid,cate))
            if catestr:
                cateobj = json.loads(catestr)
            else:
                cateobj = {}
            for property in v:
                if property not in cateobj:
                    cateobj[property] = {}
                if property == 'cat':
                    if len(v['cat']) > i+1 and i < len(v['cat'])-1:
                        if v['cat'][i+1] not in cateobj['cat']:
                            cateobj['cat'][(v['cat'][i+1])] = 1
                        else:
                            cateobj['cat'][(v['cat'][i+1])] += 1
                elif property == 'iid':
                    if i == len(v['cat'])-1 and v['iid'] not in cateobj['iid']:
                        cateobj['iid'][v['iid']] = 1
                elif isinstance(v[property],list):
                    for p in v[property]:
                        if p not in cateobj[property]:
                            cateobj[property][p] = 1
                        else:
                            cateobj[property][p] += 1
                else:
                    if v[property] not in cateobj[property]:
                        cateobj[property][v[property]] = 1
                    else:
                        cateobj[property][v[property]] += 1
                if len(cateobj[property]) == 0:
                    del cateobj[property]
            if catestr != json.dumps(cateobj):
                if len(cateobj) > 0:
                    cache.set('%s:index:cat%s'%(cid,cate),json.dumps(cateobj))
        # 更新属性索引
        for property in v:
            if property == 'cat' or property == 'iid':
                continue
            if isinstance(v[property],list):
                for p in v[property]:
                    pstr = cache.get('%s:index:%s:%s'%(cid,property,p))
                    if pstr:
                        pobj = json.loads(pstr)
                    else:
                        pobj = {}
                    if v['iid'] not in pobj:
                        pobj[v['iid']] = 1
                    else:
                        pobj[v['iid']] += 1
                    if pstr != json.dumps(pobj):
                        if len(pobj) > 0:
                            cache.set('%s:index:%s:%s'%(cid,property,p),json.dumps(pobj))
            else:
                p = v[property]
                pstr = cache.get('%s:index:%s:%s'%(cid,property,p))
                if pstr:
                    pobj = json.loads(pstr)
                else:
                    pobj = {}
                if v['iid'] not in pobj:
                    pobj[v['iid']] = 1
                else:
                    pobj[v['iid']] += 1
                if pstr != json.dumps(pobj):
                    if len(pobj) > 0:
                        cache.set('%s:index:%s:%s'%(cid,property,p),json.dumps(pobj))
        return True

    def PUT(self,cid,brd):
        ''' /bfdrest/client/(cid)/brand/(brd) '''
        value = web.data()
        return cache.set('%s:brand:%s' % (cid,brd),value)

    def DELETE(self,cid):
        ''' /bfdrest/client/(cid)/property '''
        value = web.data()
        value_error = '{"stat":false,"info":"Wrong json data","format":{"property":"value","property_repeat":[]}}'
        try:
            v = json.loads(value)
        except:
            return value_error

        if 'iid' not in v:
            return '{"stat":false,"info":"no iid"}'
        return delete_item(cid,v['iid'])
"""
