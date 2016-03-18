# **********************************************************************
#
# Copyright (c) 2003-2009 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

# Ice version 3.3.1
# Generated from file `KafkaConsumerClient.ice'

import Ice, IcePy, __builtin__

if not Ice.__dict__.has_key("_struct_marker"):
    Ice._struct_marker = object()

# Start of module bfd
_M_bfd = Ice.openModule('bfd')
__name__ = 'bfd'

# Start of module bfd.kafkaconsumerclient
_M_bfd.kafkaconsumerclient = Ice.openModule('bfd.kafkaconsumerclient')
__name__ = 'bfd.kafkaconsumerclient'

if not _M_bfd.kafkaconsumerclient.__dict__.has_key('RetInfo'):
    _M_bfd.kafkaconsumerclient.RetInfo = Ice.createTempClass()
    class RetInfo(Ice.Object):
        def __init__(self, message='', ret=0):
            self.message = message
            self.ret = ret

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::bfd::kafkaconsumerclient::RetInfo')

        def ice_id(self, current=None):
            return '::bfd::kafkaconsumerclient::RetInfo'

        def ice_staticId():
            return '::bfd::kafkaconsumerclient::RetInfo'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_bfd.kafkaconsumerclient._t_RetInfo)

        __repr__ = __str__

    _M_bfd.kafkaconsumerclient.RetInfoPrx = Ice.createTempClass()
    class RetInfoPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_bfd.kafkaconsumerclient.RetInfoPrx.ice_checkedCast(proxy, '::bfd::kafkaconsumerclient::RetInfo', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_bfd.kafkaconsumerclient.RetInfoPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_bfd.kafkaconsumerclient._t_RetInfoPrx = IcePy.defineProxy('::bfd::kafkaconsumerclient::RetInfo', RetInfoPrx)

    _M_bfd.kafkaconsumerclient._t_RetInfo = IcePy.defineClass('::bfd::kafkaconsumerclient::RetInfo', RetInfo, (), False, None, (), (
        ('message', (), IcePy._t_string),
        ('ret', (), IcePy._t_int)
    ))
    RetInfo.ice_type = _M_bfd.kafkaconsumerclient._t_RetInfo

    _M_bfd.kafkaconsumerclient.RetInfo = RetInfo
    del RetInfo

    _M_bfd.kafkaconsumerclient.RetInfoPrx = RetInfoPrx
    del RetInfoPrx

if not _M_bfd.kafkaconsumerclient.__dict__.has_key('_t_RetInfoSeq'):
    _M_bfd.kafkaconsumerclient._t_RetInfoSeq = IcePy.defineSequence('::bfd::kafkaconsumerclient::RetInfoSeq', (), _M_bfd.kafkaconsumerclient._t_RetInfo)

if not _M_bfd.kafkaconsumerclient.__dict__.has_key('KafkaConsumerClientManager'):
    _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager = Ice.createTempClass()
    class KafkaConsumerClientManager(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager:
                raise RuntimeError('bfd.kafkaconsumerclient.KafkaConsumerClientManager is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::bfd::kafkaconsumerclient::KafkaConsumerClientManager')

        def ice_id(self, current=None):
            return '::bfd::kafkaconsumerclient::KafkaConsumerClientManager'

        def ice_staticId():
            return '::bfd::kafkaconsumerclient::KafkaConsumerClientManager'
        ice_staticId = staticmethod(ice_staticId)

        #
        # Operation signatures.
        #
        # def getUserID(self, current=None):
        # def close(self, topic, group, userid, current=None):
        # def closeAndDelete(self, topic, group, userid, current=None):
        # def setConsumeMethod(self, group, method, current=None):
        # def get(self, topic, group, userid, current=None):
        # def getFromBegin(self, topic, group, userid, current=None):
        # def getPeriod(self, topic, group, date, userid, current=None):
        # def getPeriodFromBegin(self, topic, group, date, userid, current=None):
        # def getArray(self, topic, group, userid, seqlen, current=None):
        # def getArrayFromBegin(self, topic, group, userid, seqlen, current=None):
        # def getArrayPeriod(self, topic, group, date, userid, seqlen, current=None):
        # def getArrayPeriodFromBegin(self, topic, group, date, userid, seqlen, current=None):
        # def getBlock(self, topic, group, userid, current=None):
        # def getFromBeginBlock(self, topic, group, userid, current=None):
        # def getArrayBlock(self, topic, group, userid, seqlen, current=None):
        # def getArrayFromBeginBlock(self, topic, group, userid, seqlen, current=None):
        # def commitoffset(self, topic, group, userid, current=None):
        # def hadoopGet(self, topic, group, userid, current=None):
        # def hadoopGetTopicList(self, prefix, password, current=None):

        def __str__(self):
            return IcePy.stringify(self, _M_bfd.kafkaconsumerclient._t_KafkaConsumerClientManager)

        __repr__ = __str__

    _M_bfd.kafkaconsumerclient.KafkaConsumerClientManagerPrx = Ice.createTempClass()
    class KafkaConsumerClientManagerPrx(Ice.ObjectPrx):

        def getUserID(self, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getUserID.invoke(self, ((), _ctx))

        def close(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_close.invoke(self, ((topic, group, userid), _ctx))

        def closeAndDelete(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_closeAndDelete.invoke(self, ((topic, group, userid), _ctx))

        def setConsumeMethod(self, group, method, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_setConsumeMethod.invoke(self, ((group, method), _ctx))

        def get(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_get.invoke(self, ((topic, group, userid), _ctx))

        def getFromBegin(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getFromBegin.invoke(self, ((topic, group, userid), _ctx))

        def getPeriod(self, topic, group, date, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getPeriod.invoke(self, ((topic, group, date, userid), _ctx))

        def getPeriodFromBegin(self, topic, group, date, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getPeriodFromBegin.invoke(self, ((topic, group, date, userid), _ctx))

        def getArray(self, topic, group, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArray.invoke(self, ((topic, group, userid, seqlen), _ctx))

        def getArrayFromBegin(self, topic, group, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArrayFromBegin.invoke(self, ((topic, group, userid, seqlen), _ctx))

        def getArrayPeriod(self, topic, group, date, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArrayPeriod.invoke(self, ((topic, group, date, userid, seqlen), _ctx))

        def getArrayPeriodFromBegin(self, topic, group, date, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArrayPeriodFromBegin.invoke(self, ((topic, group, date, userid, seqlen), _ctx))

        def getBlock(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getBlock.invoke(self, ((topic, group, userid), _ctx))

        def getFromBeginBlock(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getFromBeginBlock.invoke(self, ((topic, group, userid), _ctx))

        def getArrayBlock(self, topic, group, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArrayBlock.invoke(self, ((topic, group, userid, seqlen), _ctx))

        def getArrayFromBeginBlock(self, topic, group, userid, seqlen, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_getArrayFromBeginBlock.invoke(self, ((topic, group, userid, seqlen), _ctx))

        def commitoffset(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_commitoffset.invoke(self, ((topic, group, userid), _ctx))

        def hadoopGet(self, topic, group, userid, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_hadoopGet.invoke(self, ((topic, group, userid), _ctx))

        def hadoopGetTopicList(self, prefix, password, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager._op_hadoopGetTopicList.invoke(self, ((prefix, password), _ctx))

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManagerPrx.ice_checkedCast(proxy, '::bfd::kafkaconsumerclient::KafkaConsumerClientManager', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_bfd.kafkaconsumerclient.KafkaConsumerClientManagerPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_bfd.kafkaconsumerclient._t_KafkaConsumerClientManagerPrx = IcePy.defineProxy('::bfd::kafkaconsumerclient::KafkaConsumerClientManager', KafkaConsumerClientManagerPrx)

    _M_bfd.kafkaconsumerclient._t_KafkaConsumerClientManager = IcePy.defineClass('::bfd::kafkaconsumerclient::KafkaConsumerClientManager', KafkaConsumerClientManager, (), True, None, (), ())
    KafkaConsumerClientManager.ice_type = _M_bfd.kafkaconsumerclient._t_KafkaConsumerClientManager

    KafkaConsumerClientManager._op_getUserID = IcePy.Operation('getUserID', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (), (), IcePy._t_long, ())
    KafkaConsumerClientManager._op_close = IcePy.Operation('close', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), None, ())
    KafkaConsumerClientManager._op_closeAndDelete = IcePy.Operation('closeAndDelete', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), None, ())
    KafkaConsumerClientManager._op_setConsumeMethod = IcePy.Operation('setConsumeMethod', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_int)), (), IcePy._t_int, ())
    KafkaConsumerClientManager._op_get = IcePy.Operation('get', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getFromBegin = IcePy.Operation('getFromBegin', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getPeriod = IcePy.Operation('getPeriod', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getPeriodFromBegin = IcePy.Operation('getPeriodFromBegin', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getArray = IcePy.Operation('getArray', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_getArrayFromBegin = IcePy.Operation('getArrayFromBegin', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_getArrayPeriod = IcePy.Operation('getArrayPeriod', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_getArrayPeriodFromBegin = IcePy.Operation('getArrayPeriodFromBegin', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_getBlock = IcePy.Operation('getBlock', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getFromBeginBlock = IcePy.Operation('getFromBeginBlock', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_getArrayBlock = IcePy.Operation('getArrayBlock', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_getArrayFromBeginBlock = IcePy.Operation('getArrayFromBeginBlock', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long), ((), IcePy._t_int)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())
    KafkaConsumerClientManager._op_commitoffset = IcePy.Operation('commitoffset', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), None, ())
    KafkaConsumerClientManager._op_hadoopGet = IcePy.Operation('hadoopGet', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_long)), (), _M_bfd.kafkaconsumerclient._t_RetInfo, ())
    KafkaConsumerClientManager._op_hadoopGetTopicList = IcePy.Operation('hadoopGetTopicList', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string)), (), _M_bfd.kafkaconsumerclient._t_RetInfoSeq, ())

    _M_bfd.kafkaconsumerclient.KafkaConsumerClientManager = KafkaConsumerClientManager
    del KafkaConsumerClientManager

    _M_bfd.kafkaconsumerclient.KafkaConsumerClientManagerPrx = KafkaConsumerClientManagerPrx
    del KafkaConsumerClientManagerPrx

# End of module bfd.kafkaconsumerclient

__name__ = 'bfd'

# End of module bfd
