import baostock as bs
import pandas as pd
import datetime
import time

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def hangye():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取行业分类数据
    rs = bs.query_stock_industry()
    # rs = bs.query_stock_basic(code_name="浦发银行")
    print('query_stock_industry error_code:' + rs.error_code)
    print('query_stock_industry respond  error_msg:' + rs.error_msg)

    # 打印结果集
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv("C:\\gupiao\\行业分类.csv", encoding="gbk", index=False)
    print(result)

    # 登出系统
    bs.logout()

def gegu(code, name):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date='1900-01-01', end_date='2100-12-31',
                                      frequency="d", adjustflag="2")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        thedata = rs.get_row_data()

        #添加月份
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(thedata[0], "%Y-%m-%d")))
        weekday = date.isoweekday()
        thedata.append(weekday.__str__())
        month = date.month
        thedata.append(month.__str__())
        mouthday = date.day
        thedata.append(mouthday.__str__())

        data_list.append(thedata)
    rs.fields.append("周几")
    rs.fields.append("几月")
    rs.fields.append("几号")
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("C:\\gupiao\\" + name + ".csv", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()


if __name__ == '__main__':
    gegu(code="sz.002156",name="通富微电")
    # hangye()


