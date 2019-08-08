import os
import time
import unittest

from base.HTMLTestRunner_cn import HTMLTestRunner
def run_all_case():
    p_path=os.getcwd().split("main")[0]
    print(p_path)
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    reportfile = os.path.join(p_path,"report",now_time + "result.html")
    test_app=os.path.join(p_path,"case")
    fp = open(reportfile, 'wb')
    runner = HTMLTestRunner(fp,
                            title="数据资产管理系统-测试报告",
                             )
    discover = unittest.defaultTestLoader.discover(test_app , pattern='*_case.py')

    runner.run(discover)
    fp.close()



if __name__ == '__main__':

    run_all_case()