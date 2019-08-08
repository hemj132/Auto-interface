# coding:utf-8
import testdata as testdata

from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependdentData
from util.operation_header import OperationHeader
from util.operation_json import OperetionJson
import unittest
from ddt import ddt, data, unpack

case_lists=GetData().get_case_list()
@ddt
class main_case(unittest.TestCase):


    def setUp(self):
        self.run_method = RunMethod()
        self.com_util = CommonUtil()
    @data(*case_lists)
    @unpack
    def test_main(self,sheet_name,case_name,sheet_id,case_id):
        self.data = GetData(sheet_id)
        i=case_id
        is_run = self.data.get_is_run(i)
        if is_run:
            url = self.data.get_request_url(i)
            method = self.data.get_request_method(i)

            #request_data = self.data.get_data_for_json(i)
            request_data = self.data.get_request_data(i)
            # expect = self.data.get_expcet_data_for_mysql(i)
            expect = self.data.get_expcet_data(i)
            header = self.data.is_header(i)
            depend_case = self.data.is_depend(i)
            if depend_case != None:
                self.depend_data = DependdentData(sheet_id, depend_case)
                # 获取的依赖响应数据
                depend_response_data = self.depend_data.get_data_for_key(i)
                # 获取依赖的key
                depend_key = self.data.get_depend_field(i)
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
            if self.com_util.is_contain(expect, res):
                self.data.write_result(i, 'pass')

            else:
                self.data.write_result(i, res)
            #self.assertIn(expect,res,"预期结果：{0} 未在实际返回结果：{1} 中！ ".format(expect,res))
            self.assertIn(expect,res)


if __name__ == '__main__':
    unittest.main(verbosity=2)