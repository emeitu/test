# -*- coding=utf-8 -*-

import web
import json
import libcache as cache

urls = ['/bfdrest/clients/(.+)/collocations/(.+)']

post_data ={
"categorys":[[""]],
"brands":[[""]],
"goods":[
    {
        "ItemID":"",
        "ItemTitle":"",
        "ImageURL":"",
        "BrandName":[""],
        "CategoryName":[""],
        "Price":0.0,
        "Content":"",
        "Color":[""]
    }
]
}

post_data_ret = {
"stat":False,
"categorys":0,
"brands":0,
"goods":{
    "create":[],
    "update":[],
    "fail":[]
}
}

get_data_ret = post_data_ret

delete_data_ret = {"stat":True}

class handler:
    def GET(self,cid,colid):
        ''' /bfdrest/(cid)/collocations/(colid) '''
        ret = get_data_ret
        if cache.get('%s:goods:%s' % (cid,goodsid)):
            ret["stat"]=True
        else:
            pass
        return json.dumps(ret)

    def POST(self,cid,colid):
        ''' /bfdrest/(cid)/collocations/(colid) '''
        value = web.data()
        ret = post_data_ret
        if cache.set('%s:goods:%s' % (cid,goodsid),value):
            ret["stat"]=True
        else:
            pass
        return json.dumps(ret)

    def PUT(self,cid,col):
        ''' /bfdrest/(cid)/collocations/(colid) '''
        value = web.data()
        ret = post_data_ret
        if cache.set('%s:goods:%s' % (cid,goodsid),value):
            ret["stat"]=True
        else:
            pass
        return json.dumps(ret)

    def DELETE(self,cid,col):
        ''' /bfdrest/(cid)/collocations/(colid) '''
        ret = delete_data_ret
        if cache.delete('%s:goods:%s' % (cid,goodsid)):
            ret["stat"]=True
        else:
            pass
        return json.dumps(ret)

