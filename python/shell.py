#!/usr/bin/env python
# coding=utf-8

import os
import logging
import commands

cmd='ls -l /home'
cmd1='ls -l /home/ls'
#code=os.system('ls /home/ls')

code,content=commands.getstatusoutput(cmd1)


print "code:",code," content:",content

logging.debug("code:%s  content:%s",code, content)


