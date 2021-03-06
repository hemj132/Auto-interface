#coding:utf-8
import pymysql
import json
from util.configReader import YamlReader
class OperationMysql:
	def __init__(self):
		self.host = YamlReader().data['mysqldb']['ip']
		self.port = int(YamlReader().data['mysqldb']['port'])
		self.user = YamlReader().data['mysqldb']['username']
		self.passwd = YamlReader().data['mysqldb']['password']
		self.db = YamlReader().data['mysqldb']['defaultDB']
		self.conn = pymysql.connect(
			host=self.host,
			port=self.port,
			user=self.user,
			passwd=self.passwd,
			db=self.db,
			charset='utf8'

			)
		self.cur = self.conn.cursor()

	#查询一条数据
	#查询条数据
	def search_one(self,sql):
		#self.cur.execute(sql)
		#断开会重连？？？
		self.conn.ping(reconnect=True)
		self.cur.execute(sql)
		self.conn.commit()

		result = self.cur.fetchall()
		self.conn.close()

		if result == None :
			return result
		elif  len(result)==0:
			return None
		else:

			#只有一条记录，
			if len(result)==1:

				#一条记录只有一列，提前解包
				if len(*result)==1:
					print("{0}====={1}".format(sql,result[0][0]))

					return result[0][0]
				else:
					#一条记录多列，返回一个元组
					print("{0}====={1}".format(sql, result[0]))
					return result[0]
			#多条记录，不做处理
			return result


if __name__ == '__main__':
	op_mysql = OperationMysql()
	res = op_mysql.search_one("SELECT usercode FROM ds_sys_user LIMIT 1")
	#print res
