#coding:utf-8
from util.operation_excel import OperationExcel
from  data import  data_config
#import data_config
from util.operation_json import OperetionJson
from util.connect_db import OperationMysql
import re
from util.configReader import BASE_PATH,YamlReader
import os
import json
class GetData():
	def __init__(self,sheet_id=0):
		self.file_name =os.path.join(BASE_PATH,YamlReader().data["global"]["case_path"])
		self.opera_excel = OperationExcel(file_name=self.file_name,sheet_id=sheet_id)

	#获取sheet名字
	def get_sheet_names(self):
		return self.opera_excel.get_sheet()

	#去获取excel行数,就是我们的case个数
	def get_case_lines(self):
		return self.opera_excel.get_lines()

	#获取是否执行
	def get_is_run(self,row):
		flag = None
		col = int(data_config.get_run())
		run_model = self.opera_excel.get_cell_value(row,col)
		if run_model == 'yes':
			flag = True
		else:
			flag = False
		return flag

	#是否携带header
	def is_header(self,row):
		col = int(data_config.get_header())
		header = self.opera_excel.get_cell_value(row,col)
		if header != '':
			return header
		else:
			return None

	#获取请求方式
	def get_request_method(self,row):
		col = int(data_config.get_run_way())
		request_method = self.opera_excel.get_cell_value(row,col)
		return request_method

	#获取url
	def get_request_url(self,row):
		col = int(data_config.get_url())
		url = self.opera_excel.get_cell_value(row,col)
		return url

	#获取请求数据
	def get_request_data(self,row):
		col = int(data_config.get_data())
		data = self.opera_excel.get_cell_value(row,col)
		if data == '':
			return None
		#替换
		p = r"\${(.+?)}"
		robocop = re.compile(p, re.I)
		temps = robocop.findall(data)
		if temps:
			for temp in temps:
				# 数据库查询,不区分大小写
				if temp.upper().find("select".upper()) >= 0:
					op_mysql = OperationMysql()
					res = op_mysql.search_one(temp)
					data = re.sub(p, res, data)
				# json替换
				else:
					opera_json = OperetionJson()
					res = str(opera_json.get_data(temp))
					data = re.sub(p, res, data)

		print(data)
		return eval(data)

	#通过获取关键字拿到data数据
	def get_data_for_json(self,row):
		opera_json = OperetionJson()
		request_data = opera_json.get_data(self.get_request_data(row))
		return request_data

	#获取预期结果
	def get_expcet_data(self,row):
		col = int(data_config.get_expect())
		expect = self.opera_excel.get_cell_value(row,col)
		if expect == '':
			return None
		# 替换
		p = r"\${(.+?)}"
		robocop = re.compile(p, re.I)
		temps = robocop.findall(expect)
		if temps:
			for temp in temps:
				# 数据库查询,不区分大小写
				if temp.upper().find("select".upper()) >= 0:
					op_mysql = OperationMysql()
					res = op_mysql.search_one(temp)
					expect = re.sub(p, res, expect)
				# json替换
				else:
					opera_json = OperetionJson()
					res = str(opera_json.get_data(temp))
					expect = re.sub(p, res, expect)

		return expect

	#通过sql获取预期结果
	def get_expcet_data_for_mysql(self,row):
		op_mysql = OperationMysql()
		sql = self.get_expcet_data(row)
		res = op_mysql.search_one(sql)
		return res

	def write_result(self,row,value):
		col = int(data_config.get_result())
		self.opera_excel.write_value(row,col,value)

	#获取依赖数据的key
	def get_depend_key(self,row):
		col = int(data_config.get_data_depend())
		depent_key = self.opera_excel.get_cell_value(row,col)
		if depent_key == "":
			return None
		else:
			return depent_key

	#判断是否有case依赖
	def is_depend(self,row):
		col = int(data_config.get_case_depend())
		depend_case_id = self.opera_excel.get_cell_value(row,col)
		if depend_case_id == "":
			return None
		else:
			return depend_case_id

	#获取数据依赖字段
	def get_depend_field(self,row):
		col = int(data_config.get_field_depend())
		data = self.opera_excel.get_cell_value(row,col)
		if data == "":
			return None
		else:
			return data

		# 是否携带header
	def get_case_name(self, row):
			col = int(data_config.get_case_name())
			case_name = self.opera_excel.get_cell_value(row, col)
			if case_name != '':
				return case_name
			else:
				return None
	#这是加ddt打的补丁，所以看起来有点诡异
	def get_case_list(self):
			case_list = []
			sheet_names = self.get_sheet_names()
			for sheet_id in range(len(sheet_names)):
				data = GetData(sheet_id)
				rows_count = data.get_case_lines()
				for i in range(1, rows_count):
					#是否运行
					if data.get_is_run(i):
						case_name = data.get_case_name(i)
						case_list.append([sheet_names[sheet_id] ,case_name,sheet_id,i])
			return case_list





