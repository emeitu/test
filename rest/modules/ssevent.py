# -*- coding=utf-8 -*-

import os
import web
import json
import time
import kafkaData

urls = ['/ssevent/(.*)']

class handler:
    def GET(self,method=None):
        ''' '/ssevent/(.*)' '''
        args = web.input()
        web.header('Content-Type', 'text/event-stream')
        web.header('Cache-Control', 'no-cache')
        if method == 'demo':
            return 'data: %s\n\n'%time.time()
        elif method == 'kafka':
            topic = args.get('topic')
            group = args.get('group')
            regex = args.get('regex')
            return 'data: %s\n\n'%kafkaData.getData(topic,group,regex)
        else:
            return method

    def POST(self,method=None):
        ''' '/demo','/demo/(.+)' '''
        data = web.data()
        return 'OK, data: %s' % str(data)

