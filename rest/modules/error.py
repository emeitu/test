# -*- coding=utf-8 -*-

import os
import web
import json
import urllib2
import libmysql
from libpub import error_logger
from libpub import callback

urls = ['/error/(log)/(.*)','/error/(read)/(.*)','/error']
mysql = libmysql.BfdMysql()

class handler:
    def GET(self,method=None,num=10):
        ''' '/error/(log)/(nums)','/error' '''
        if method == 'log':
            num=int(num)
            log = []
            log.extend(urllib2.urlopen('http://192.168.49.90:9090/error/read/%d'%num).readlines())
            log.extend(urllib2.urlopen('http://192.168.49.91:9090/error/read/%d'%num).readlines())
            return ''.join(sorted(log)[-num:])
        if method == 'read':
            num=int(num)
            log = open('bfdrest_error.log','r').readlines()[-num:]
            return ''.join(log)
        args = web.input()
        env = web.ctx['env']
        def parsedict(d):
            if isinstance(d,dict):
                r = {}
                for key in d:
                    r[key] = parsedict(d[key])
                return r
            else:
                return str(d)
        ret = {
        'args':args,
        'HTTP_COOKIE':parsedict(env['HTTP_COOKIE']),
        'HTTP_USER_AGENT':parsedict(env['HTTP_USER_AGENT']),
        'HTTP_X_REAL_IP':parsedict(env['HTTP_X_REAL_IP']),
        #'HTTP_X_REAL_IP':parsedict(env['REMOTE_ADDR']),
        }
        cookies = ret['HTTP_COOKIE'].split(';')
        gid=''
        for i in xrange(len(cookies)):
            cookie = cookies[i].strip()
            if cookie.startswith('bfdid='):
                gid=cookie[6:]
        ip = ret['HTTP_X_REAL_IP']
        user_agent = ret['HTTP_USER_AGENT']
        msg = ret['args'].get('msg')
        error_logger.info(json.dumps(ret))
        sql = "insert into error_msg (gid,ip,user_agent,msg) values ('%s','%s','%s','%s')"%(gid,ip,user_agent,msg)
        print sql
        mysql.execute(sql)
        return callback('[0,"OK"]')

    def POST(self,method=None):
        ''' '/demo','/demo/(.+)' '''
        data = web.data()
        return 'OK, data: %s' % str(data)

