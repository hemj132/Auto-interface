2019-08-07

main
    main/run_test.py 不带报告
    main/unittest_run.py 会生成html报告
用例存放在data/case1.xls
    请求数据与预期结果 支持读取json/sql
    json存放在user.json
    以${}标识，大括号内为json名称，若大括号内有关键字select（不区分大小写），则判断为sql；查询后再拼装
cookie需具体项目再处理。
