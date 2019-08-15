# coding:utf-8
import time
from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependdentData
from util.operation_header import OperationHeader
from util.operation_json import OperetionJson
import unittest
from ddt import ddt, data, unpack

case_list=GetData().get_case_list()
@ddt
class MainCase(unittest.TestCase):


    def setUp(self):
        self.run_method = RunMethod()
        self.com_util = CommonUtil()
    @data(*case_list)
    @unpack
    def test_main(self, sheet_name, case_name, sheet_id, case_id):
        self.data = GetData(sheet_id)
        is_run = self.data.get_is_run(case_id)
        if is_run:
            url = self.data.get_request_url(case_id)
            method = self.data.get_request_method(case_id)

            #request_data = self.data.get_data_for_json(i)
            request_data = self.data.get_request_data(case_id)
            # expect = self.data.get_expcet_data_for_mysql(i)
            expect = self.data.get_expcet_data(case_id)
            header = self.data.is_header(case_id)
            depend_case = self.data.is_depend(case_id)
            if depend_case != None:
                self.depend_data = DependdentData(sheet_id, depend_case)
                # 获取的依赖响应数据
                depend_response_data = self.depend_data.get_data_for_key(case_id)
                # 获取依赖的key
                depend_key = self.data.get_depend_field(case_id)
                request_data[depend_key] = depend_response_data
            if header == 'write':
                res = self.run_method.run_main(method, url, request_data)
                op_header = OperationHeader(res)
                op_header.write_cookie()

            elif header == 'yes':
                op_json = OperetionJson('../dataconfig/cookie.json')
                cookie = op_json.get_data('apsid')
                cookies = {
                    'apsid': cookie
                }
                res = self.run_method.run_main(method, url, request_data, cookies)
            else:
                res = self.run_method.run_main(method, url, request_data)
            print(res)
            if self.com_util.is_contain(expect, res):
                self.data.write_result(case_id,'pass')

            else:
                self.data.write_result(case_id, res)
            #self.assertIn(expect,res,"预期结果：{0} 未在实际返回结果：{1} 中！ ".format(expect,res))
            #添加最后结果时间戳
            self.data.write_result(0,  '实际结果 {}'.format(time.strftime("%Y_%m_%d_%H_%M_%S")))
            self.assertIn(expect,res)


if __name__ == '__main__':
    unittest.main(verbosity=2)