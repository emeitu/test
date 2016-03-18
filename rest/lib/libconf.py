# -*- coding=utf-8 -*-

conf_ = {
    "Cdemo":{
        "main_property"   : "pid",
        "properties" : ["pid","brand"],
        "tree_deep" : 4
    },
    "Czouxiu":{
        "main_property"   : "pid",
        "properties" : ["pid","brand"],
        "tree_deep" : 4
    },
    "Ctest_ifec":{
        "main_property"   : "pid",
        "properties" : ["pid","brand"],
        "tree_deep" : 4
    }
}

def get_conf(client):
    if client in conf_:
        return conf_[client]
    else:
        return {}

def get_all_conf():
    return conf_

