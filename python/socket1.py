#!/usr/bin/env python
# coding=utf-8

import struct
import socket
import bisect
import logging


def searchIp(ip):
    ip_int = int(socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0]))
    ip_int  =  16823040
    place = ''
    index = bisect.bisect_left(keys, (ip_int, ip_int))
    if (index == length) :
        pass 
    elif ((ip_int >=keys[index-1][0]) and (ip_int <= keys[index-1][1])  ) :
        place = location[keys[index-1]]
    elif ((ip_int >=keys[index][0]) and (ip_int <= keys[index][1])  ) :
        place = location[keys[index]]
    else :
        pass
    logging.info("ip=%s, place=%s" % (ip,place))
    if place =='':
        print "can not find place"
    else :    
        print ip, place

def Loaddata():
    location={}
    fp=open("ip_city.txt")
    lines=fp.readlines()
    count = 0;
    for line in lines: 
        length=len(line)
        pos1=line.find(',', 0);
        if (pos1 != (length-1)) :
            startStr=line[0:pos1]
            ip_start=int(startStr)
        pos2=line.find(',', pos1+1)
        if (pos2 != (length-1)) :
            endStr=line[pos1+1:pos2]
            ip_end=int(endStr)
        place=line[pos2+1:]
        place.strip("\n")
        place_decode=place.decode('utf-8')
        location[(ip_start,ip_end)] = place_decode
        #location[(ip_start,ip_end)] = place
        count += 1
        if (count > 10) :
            break
    fp.close()
    return location

if __name__ == "__main__" :
    location = Loaddata()
    keys = location.keys()
    length = len(keys)
    keys.sort()
    print location

    ips=["1.0.135.0", "123.34.2.12","123.34.2.255"]
    
    #searchIp(ip)
    for ip in ips :
        ip_int = int(socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0]))
        print ip,":",ip_int
    
    for i in range(9,10):
        print i

