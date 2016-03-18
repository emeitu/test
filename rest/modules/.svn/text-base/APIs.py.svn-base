# -*- coding=utf-8 -*-

import os
import web
import json

urls = ['/bfdrest/APIs','/bfdrest/APIs/(.+)']
GET_ret = {'module':[{'urls':[]},{'method':{}}]}

m_args = {}
def import_modules(modules):
    global m_args
    from imp import load_source
    for (name,file) in sorted(modules):
        m = load_source(name,file)
        m_args[name] = [{"urls":[]},{"method":{}}]
        v = dir(m)
        h, u = 'handler' in v, 'urls' in v
        if h or u:
            if not (h and u):
                raise ImportError('module %s doesn\'t have matched handler and urls' % name)
            m_args[name][0]["urls"] = m.urls
            hs = dir(m.handler)
            for method in ["GET","POST","PUT","DELETE"]:
                if method in hs:
                    m_args[name][1]["method"][method] = {}
                    m_args[name][1]["method"][method]['note'] = eval('m.handler.%s.__doc__'%method)
                    data = '%s_data' % method
                    ret = '%s_ret' % method
                    if data in v:
                        m_args[name][1]["method"][method][data] = eval('m.%s_data' % method)
                    if ret in v:
                        m_args[name][1]["method"][method][ret] = eval('m.%s_ret' % method)
    return m_args

curr_path = "modules"
modules = [(x[:-3], os.path.join(curr_path, x)) for x in os.listdir(curr_path) if x.endswith('.py')]

class handler:
    def GET(self,api=None):
        ''' /bfdrest/APIs/(api) '''
        global m_args
        if len(m_args) == 0:
            m_args = import_modules(modules)
        if not api:
            ret = []
            for m in sorted(m_args):
                ret.append({m:m_args[m]})
            return json.dumps(ret)
        elif api in m_args:
            return json.dumps(m_args[api])
        else:
            web.seeother('/bfdrest/APIs')

