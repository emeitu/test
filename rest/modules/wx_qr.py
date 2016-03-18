# -*- coding=utf-8 -*-

import web
import json
import libcache as cache
import libpub as pub
import libconf as conf
from libpub import LOG
import uuid
import urllib
import urllib2

urls = ['/wx/qr']

class handler:
    def GET(self):
        ''' '/wx/qr' '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        args = web.input()
        if "method" in args:
            method = args["method"]
            if method == "getQrTicket":
                web.header('Content-Type', 'application/javascript')
                data = args["data"]
                ret = urllib2.urlopen(
                "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=FoYOQEtQ-QHjnSv9tPDqpGOA49AFUZNqnQtPhhlRq_8i9XfxII3ofQGVtYpB6rjv",
                data)
                retstr = ret.read()
                return pub.callback(retstr,myuuid)
            elif method == "getQr":
                gid = web.cookies().get("bfdid")
                print gid
                param_index = int(cache.get("G:weixin:paramindex"))
                web.header('Content-Type', 'image/png')
                if param_index == None:
                    param_index = 0
                    cache.set("G:weixin:paramindex","0")
                else:
                    param_index = (int(param_index) + 1)%100
                    cache.set("G:weixin:paramindex",str(param_index))
                access_token = cache.get("G:weixin:access_token")
                data = {"expire_seconds":"1800","action_name":"QR_SCENE","action_info":{"scene":{"scene_id":str(param_index)}}}
                def getTicket(access_token):
                    ret = urllib2.urlopen(
                    "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token="+access_token,
                    json.dumps(data))
                    retstr = ret.read()
                    ticket = json.loads(retstr)["ticket"]
                    return ticket
                try:
                    ticket = getTicket(access_token)
                except:
                    appid = "wx68cc9091ef2be695"
                    secret = "c27b72cd1d51114cda5e816bbb95ab6d"
                    get_access_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid,secret)
                    access_token_ret = urllib2.urlopen(get_access_url)
                    access_token = json.loads(access_token_ret.read())["access_token"]
                    cache.set("G:weixin:access_token",access_token)
                    ticket = getTicket(access_token)
                    
                qrurl = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"%ticket
                qrimg = urllib2.urlopen(qrurl)
                img = qrimg.read()
                cache.set("G:weixin:scene:%d"%param_index,gid)
                return img
            elif method == "getgid":
                web.header('Content-Type', 'application/javascript')
                open_id = args["open_id"]
                cid = args["cid"]
                if "scene_id" in args:
                    scene_id = args["scene_id"]
                    gid = cache.get("G:weixin:scene:%s"%scene_id)
                    cache.set("G:weixin:openid:%s:%s"%(cid,open_id),gid)
                    return pub.callback('"%s"'%gid,myuuid)
                else:
                    gid = cache.get("G:weixin:openid:%s:%s"%(cid,open_id))
                    return pub.callback('"%s"'%gid,myuuid)
            elif method == "getopenid":
                web.header('Content-Type', 'application/javascript')
                code = args['code']
                access_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx68cc9091ef2be695&secret=c27b72cd1d51114cda5e816bbb95ab6d&code=%s&grant_type=authorization_code' % code
                ret = urllib2.urlopen(access_url)
                return pub.callback(ret.read(),myuuid)

        else:
            web.header('Content-Type', 'application/javascript')
            return pub.callback(json.dumps(None),myuuid)
