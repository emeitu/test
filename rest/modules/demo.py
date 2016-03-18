# -*- coding=utf-8 -*-

import web
import json

urls = ['/demo','/demo/(.+)']

class handler:
    def GET(self,method=None):
        ''' '/demo','/demo/(.+)' '''
        args = web.input()
        # web.header('Content-Type', 'text/xml')
        if not method:
            return 'this is a web.py demo. %s' % (args)
        elif method == 'args':
            return 'args: %s' % args
        elif method == 'ctx': # return web.ctx
            ctxdict = web.ctx.__dict__;
            ret = {}
            def parsedict(d):
                if isinstance(d,dict):
                    r = {}
                    for key in d:
                        r[key] = parsedict(d[key])
                    return r
                else:
                    return str(d)
            for key in ctxdict:
                ret[key] = parsedict(ctxdict[key])
            return json.dumps(ret)
        else:
            return 'this is a web.py demo. method is %s. args: %s' % (method,args)

    def POST(self,method=None):
        ''' '/demo','/demo/(.+)' '''
        data = web.data()
        return 'OK, data: %s' % str(data)

