# -*- coding=utf-8 -*-

import web

urls = ['/r','/(.*)/']

class handler:
    def GET(self,path=None):
        ''' '/(.*)/' redirct to '/(.*)' '''
        if path:
            web.seeother('/'+path)
            return
        else:
            args = web.input()
            if 'url' in args:
                web.found(args['url'])

    def PUT(self,path=None):
        ''' '/(.*)/' redirct to '/(.*)' '''
        if path:
            web.seeother('/'+path)
            return

    def POST(self,path=None):
        ''' '/(.*)/' redirct to '/(.*)' '''
        if path:
            web.seeother('/'+path)
            return

    def DELETE(self,path=None):
        ''' '/(.*)/' redirct to '/(.*)' '''
        if path:
            web.seeother('/'+path)
            return
