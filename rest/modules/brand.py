# -*- coding=utf-8 -*-

import web
import json
import libcache as cache

urls = ['/bfdrest/client/(.+)/brand/(.+)','/bfdrest/client/(.+)/brand']

PUT_data = POST_data = {"brand":["brand1","brand2"],"category":["cate1","cate2"]}

PUT_ret = POST_ret = 'True|False'

GET_ret = [{'brand':[]}]

DELETE_ret = 'True|False'

class handler:
    def GET(self,cid,brd):
        '''  
            /bfdrest/client/(cid)/brand/(brd)/all for get all children;
            /bfdrest/client/(cid)/brand/(brd) for get brand's child;
            /bfdrest/client/Czouxiu/brand/_all_(/all) for example;
        '''
        if method == None:
            return cache.get('%s:brand:%s' % (cid,brd))
        elif method == 'all':
            def getbrd(brd):
                ret = []
                brdstr = cache.get('%s:brand:%s' % (cid,brd))
                try:
                    brd = json.loads(brdstr)
                    for c in brd:
                        ret.append({c:getbrd('%s:%s'%(brd,c))})
                    return ret
                except:
                    return []
            return json.dumps(getbrd(brd))

    def POST(self,cid):
        ''' /bfdrest/client/(cid)/brand '''
        value = web.data()
        value_error = '{"stat":false,"info":"Wrong json data","format":{"brand":["brand1","brand2"],"category":["cate1","cate2"]}}'
        try:
            v = json.loads(value)
        except:
            return "json error:" + value_error + value
        if 'brand' not in v or 'category' not in v:
            return value_error
        
        if len(v['category']) > 0 and v['category'][0] == '_all_':
            v['category'] = v['category'][1:]
        cates = v['category']
        brands = v['brand']
# 更新_all_的子品牌和子类目
        cate = "_all_"
        catestr = cache.get(u'%s:category:%s'%(cid,cate))
        if catestr:
            cateobj = json.loads(catestr)
        else:
            cateobj = {'brand':[],'category':[]}
        for brand in brands:
            if brand not in cateobj['brand']:
                cateobj['brand'].append(brand)
        if len(cates) > 0 and cates[0] not in cateobj['category']:
            cateobj['category'].append(cates[0])
        cache.set('%s:category:%s'%(cid,cate.decode('utf8')),json.dumps(cateobj))
# 更新各级类目的子品牌和子类目
        for i in range(len(cates)):
            cate = cate + ':' + cates[i]
            catestr = cache.get(u'%s:category:%s'%(cid,cate))
            if catestr:
                cateobj = json.loads(catestr)
            else:
                cateobj = {'brand':[],'category':[]}
            for brand in brands:
                if brand not in cateobj['brand']:
                    cateobj['brand'].append(brand)
            if len(cates) > i+1 and cates[i+1] not in cateobj['category']:
                cateobj['category'].append(cates[i+1])
            cache.set('%s:category:%s'%(cid,cate),json.dumps(cateobj))
            
        ret = json.loads(cache.get('%s:category:%s' % (cid,cate)))
        ret['category'] = cates
        return json.dumps(ret)

    def PUT(self,cid,brd):
        ''' /bfdrest/client/(cid)/brand/(brd) '''
        value = web.data()
        return cache.set('%s:brand:%s' % (cid,brd),value)

    def DELETE(self,cid,brd):
        ''' /bfdrest/client/(cid)/brand/(brd) '''
        return cache.delete('%s:brand:%s' % (cid,brd))

