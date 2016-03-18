# -*- coding=utf-8 -*-

import web
import json

urls = ['/rule/view']

class handler:
    def GET(self):
        ''' '/web' '''
        args = web.input()
        web.header('Content-Type', 'text/html; charset=utf-8')
        if not file:
            file = 'index.html'
	return ''.join(open('./web/%s'%file,'r').readlines())

    def POST(self,method=None):
        ''' '/web','/web/(.+)' '''
        data = web.data()
        return 'OK, data: %s' % str(data)

