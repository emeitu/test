# -*- coding=utf-8 -*-

import web
import logging
import uuid

proto_field_type={
    1   : "TYPE_DOUBLE",
    2   : "TYPE_FLOAT",
    3   : "TYPE_INT64",
    4   : "TYPE_UINT64",
    5   : "TYPE_INT32",
    6   : "TYPE_FIXED64",
    7   : "TYPE_FIXED32",
    8   : "TYPE_BOOL",
    9   : "TYPE_STRING",
    10  : "TYPE_GROUP",
    11  : "TYPE_MESSAGE",
    12  : "TYPE_BYTES",
    13  : "TYPE_UINT32",
    14  : "TYPE_ENUM",
    15  : "TYPE_SFIXED32",
    16  : "TYPE_SFIXED64",
    17  : "TYPE_SINT32",
    18  : "TYPE_SINT64"
}

def callback(info,myuuid = uuid.uuid1()):
    LOG("return",info,myuuid)
    data = web.input()
    if 'callback' in data:
        web.header('Content-Type', 'application/x-javascript; charset=utf-8')
        return '%s(%s)' % (data['callback'],info)
    else:
        return info

logfile = "bfdrest.log"
errlogfile = "bfdrest_error.log"
def init_log(logfile):
    logger = logging.getLogger(logfile)
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

logger = init_log(logfile)
error_logger = init_log(errlogfile)

def LOG(method,message = None,_myuuid = uuid.uuid1()):
    if method == "info":
        data = web.ctx
        http_method = data["method"] + "      "
        http_method = http_method[0:6]
        message = " %s %s %s %s%s" % (_myuuid,http_method,data["ip"],data["realhome"],data["fullpath"])
        logger.info(message)
        if web.data():
            message = "%s DATA   %s" % (_myuuid,web.data())
            logger.debug(message)
    elif method == "return":
        message = "%s RETURN %s" % (_myuuid,message)
        logger.debug(message)
