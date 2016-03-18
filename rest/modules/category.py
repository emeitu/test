# -*- coding=utf-8 -*-

import web
import json
import cPickle
import copy
import libpub as pub
from libpub import LOG
import uuid

urls = ['/bfdrest/client/(.+)/category/(.+)/(.+)','/bfdrest/client/(.+)/category/(.+)']

PUT_data = POST_data = []

PUT_ret = POST_ret = 'True|False'

GET_ret = {'success':True,'error_info':'','nodes':{},'property':[]}
GET_ret_template = {'success':True,'error_info':''}

#Node = {'categories':[],'brands':[],'nodes':Node}
node = {'categories':[],'brands':[]}

GET_ret1 = {'success':True,'error_info':'item err','brands':['NIKE','美特斯邦威'],'categories':['裤子','上衣'],'nodes':{'上衣':node,'裤子':node}}
GET_ret2 = {'success':True,'error_info':'item err','brands':['NIKE'],'categories':['西裤','牛仔裤']}

DELETE_ret = 'True|False'

property_tree = cPickle.load(open('./data/Czouxiu.ptree.pkl','rb'))

client_property_tree = {}
client_property_tree["Czouxiu"] = property_tree

class handler:
    def GET(self,cid,cat,method = None):
        '''  
            /bfdrest/client/(cid)/category/(cat)/all for get all children;
            /bfdrest/client/(cid)/category/(cat) for get category's child;
            /bfdrest/client/Czouxiu/category/_all_(/all) for example;
        '''
        myuuid = uuid.uuid1();LOG("info",_myuuid=myuuid)
        #print('cid:%s,cat:%s,method;%s' %(cid,cat,method))
        def faild(info):
            ret = copy.deepcopy(GET_ret_template)
            ret['success'] = False
            ret['error_info'] = info
            return json.dumps(ret)

        tree_path = cat.split(':')
        if tree_path[0] != "_all_":
            return pub.callback(faild('No such category'),myuuid)
        if cid not in client_property_tree:
            try:
                client_property_tree[cid] = cPickle.load(open('./data/%s.ptree.pkl'%cid,'rb'))
            except:
                client_property_tree[cid] = {"nodes":{}}
        path_str = 'client_property_tree["%s"]' % cid
        for node in tree_path[1:]:
            path_str += '["nodes"][u"%s"]' % node
        try:
            #print path_str
            cur_node = eval(path_str)
        except Exception,e:
            err_info = 'No such category. key error: %s' % unicode(e.message).encode("utf-8")
            return pub.callback(faild(err_info),myuuid)
        ret = copy.deepcopy(GET_ret_template)
        if method == None:
            ret = copy.deepcopy(GET_ret_template)
            for property in cur_node:
                if property != 'nodes' and property != 'items':
                    ret[property] = sorted(cur_node[property])
            return pub.callback(json.dumps(ret),myuuid)
        elif method == 'all':
            ret = copy.deepcopy(GET_ret_template)
            def get_nodes(cur):
                nodes = {}
                for node in cur['nodes']:
                    nodes[node] = {}
                    nodes[node]['nodes'] = get_nodes(cur['nodes'][node])
                    for property in cur['nodes'][node]:
                        if property != 'nodes' and property != 'items':
                            nodes[node][property] = sorted(cur['nodes'][node][property])
                return nodes
            for property in cur_node:
                if property != 'nodes' and property != 'items':
                    ret[property] = sorted(cur_node[property])
            ret['nodes'] = get_nodes(cur_node)
            return pub.callback(json.dumps(ret),myuuid)
        else:
            return pub.callback(faild('No such method'),myuuid)



