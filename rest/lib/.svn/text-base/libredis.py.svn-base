# -*- coding=utf-8 -*-

import redis

redis_ = {}

def get(h,p,n,k):
    if (h,p,n) not in redis_:
        redis_[(h,p,n)] = redis.Redis(h,int(p),int(n))
    return redis_[(h,p,n)].get(k)

def set(h,p,n,k,v):
    if (h,p,n) not in redis_:
        redis_[(h,p,n)] = redis.Redis(h,int(p),int(n))
    return redis_[(h,p,n)].set(k,v)

