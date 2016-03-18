# -*- coding=utf-8 -*-

HOST='192.168.24.45'
USER='bfdroot'
PASSWD='qianfendian'
DB='js_error_log'
import MySQLdb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 


class BfdMysql(object):
	def __init__(self,host=HOST,user=USER,passwd=PASSWD,db=DB):
		self.connection = MySQLdb.Connect(host,user,passwd,db,charset="utf8")
		self.cursor = self.connection.cursor()

	def __del__(self):
		self.cursor.close()
		self.connection.close()

	def execute(self,sql):
		sql=sql.encode('utf-8')
		count = 0
		try:
			count= self.cursor.execute(sql)
			self.connection.commit()
			#print 'insert success'
		except Exception,e:
			#print str(e)
			try:
				self.connection = MySQLdb.Connect(HOST,USER,PASSWD,DB,charset="utf8")
				count= self.cursor.execute(sql)
				self.cursor = self.connection.cursor()
				self.connection.commit()
				#print 'rewrite success'
			except Exception,e2:
				#print str(e2)
				return (-1,'connect error')
		return (count,self.cursor.fetchall())

import sys

if __name__ == "__main__":
	mysql = BfdMysql()
	print mysql.execute("insert into error_msg (gid,ip,user_agent,msg) values ('','10.12.0.42','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36','第一方 cookie 写入成功')")
