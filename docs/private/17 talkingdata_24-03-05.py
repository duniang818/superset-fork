import os.path
from pathlib import Path

import requests
from urllib.parse import urljoin
import json
import time
import glob
import datetime
import zipfile
import tempfile
import pandas as pd
import numpy as np
from itertools import groupby
import itertools
import shutil
from dateutil.relativedelta import *

df_total = None
# 登录
def login():
    df = pd.read_csv(r'./file/user_message_wym.csv', index_col='name')
    login_url = 'http://10.167.135.80/bigdata-export/sys/login'
    header = {'Content-Type': 'application/json',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    data = {"username": df.loc['username','message'], "password": df.loc['password','message'], "remember_me": True, "captcha": df.loc['captcha','message'],
            "checkKey": df.loc['checkKey','message'], "key": df.loc['key','message'], "iv": df.loc['iv','message'],
            "secretFlag": 1}

    resp = requests.post(login_url, data=json.dumps(data), headers=header)
    resp = json.loads(resp.text)
    if resp['message'] == '登录成功':
        token = resp['result']['token']
        timestamp = resp['timestamp']
        print('登录成功')
        return (token, timestamp, '登录成功')
    else:
        print(resp['message'])


def vin_transform(vins,token):
    url = 'http://10.167.135.80/bigdata-export/DataDownload/keepVinSecret'
    header = {
        "Content-Type":"application/json;charset=UTF-8",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        'X-Access-Token': token
    }
    data = {
        "vinArray": vins
    }
    resp = requests.post(url, data=json.dumps(data), headers=header)
    resp = json.loads(resp.text)
    dic_vin={}
    for i in resp['vinList']:
        tuple_vin = i.split('	')
        vin = tuple_vin[0]
        code = tuple_vin[1]
        dic_vin[code] = vin
    return dic_vin

# 将下载后的文件名改名成VIN
def code2vin(dic_vin,file_path, decode_path):
    if glob.glob(os.path.join(file_path, '*.csv')) != []:
        print(f"读取文件1：")
        for i in glob.glob(os.path.join(file_path,'*.csv')):
            name = os.path.split(i)[1].split('_')[0]
            try:
                new = f"{decode_path}/{dic_vin[name]}.csv"
                print(f"读取文件：{i}--》{new}")
                os.rename(i, new)    # 不需要删除，是重命名的。而我这里是换了一个目录存储
            except Exception as e:
                print(str(e))
    else:
        print(f"csv文件为空，xlsx：")
        for i in glob.glob(os.path.join(file_path,'*.xlsx')):
            name = os.path.split(i)[1].split('_')[0]
            try:
                new = f"{decode_path}/{dic_vin[name]}.xlsx"
                os.rename(i, new)
            except Exception as e:
                print(str(e))


'''
返回一个列表，
list[0]['children'] == 高精度的协议
list[1]['children'] == R平台的协议
list[2]['children'] == 3.0平台协议
list[3]['children'] == 4.0平台协议
'''


def get_id_title(token, timestamp):
    url = 'http://10.167.135.80/bigdata-export/sys/permission/'
    time_token = f'getUserPermissionByToken?_t={str(timestamp)[:10]}&token={token}'

    url1 = urljoin(url, time_token)
    header = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'X-Access-Token': token
    }

    url2 = f'http://10.167.135.80/bigdata-export/CanProtocolManager/getDataItems?dataSourceType=0&_t={str(timestamp)[:10]}'
    resp = requests.get(url2, headers=header)
    if resp.status_code == 200:
        return resp.json()


'''
传入一个submit_list
0、VIN（列表形式）
1、信号id（列表形式）
2、数据起始时间（20xx-x-x xx:xx:xx）
3、数据结束时间
4、协议平台："4.0" 、"High_Precision(4.0)" = 高精度、"High_Precision(R)" = R协议
5、dataSource：数据源选择 ：'0'=30s，'1'=1s，'8'=高精度
6、token
submit_list=[VIN列表，信号id列表，起始时间，结束时间，协议平台，数据源选择，token]
'''


def submit_data(submit_list):
    s = int(str(int(time.mktime(time.strptime(submit_list[2], '%Y-%m-%d %H:%M:%S')))) + '000')
    e = int(str(int(time.mktime(time.strptime(submit_list[3], '%Y-%m-%d %H:%M:%S')))) + '000')
    data_submit = 'http://10.167.135.80//bigdata-export/DataDownload/submit'
    header1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'X-Access-Token': submit_list[6]
    }
    data = {
        'clientIp': "undefined",
        'dataDownloadOutputFormat': "Csv",
        'dataDownloadOutputStyle': "MultiFile",
        'dataDownloadType': "Template",
        'dataEndTime': e,
        'dataParseType': "0",  # "0"=不解析，"1" = 解析
        'dataSourceType': submit_list[5],
        'dataStartTime': s,
        'protocolVersion': submit_list[4],
        'selectItems': submit_list[1],
        'vinArray': submit_list[0]
    }
    resp = requests.post(url=data_submit, headers=header1, data=json.dumps(data))
    if resp.status_code == 200:
        a = resp.json()
        if 'message' in a.keys():
            print(a['message'])
        else:
            print('提交成功')
            return '提交成功'
    else:
        print(f'网页报错：{resp.status_code}')
        return '报错'


def download(token, start_time, save_path):
    dfk = pd.read_csv(r'./file/user_message_wym.csv', index_col='name')
    tell_me = ''
    download_dic = {}
    try_downloard_count = 0
    while True:
        try:
            while True:
                now = datetime.datetime.now()
                timestamp = int(time.mktime(now.timetuple()))  #timetuple 返回一个时间结构体，包含很多信息；mktime是返回以秒表示时间的浮点数
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    'X-Access-Token': token}
                url = f'http://10.167.135.80/bigdata-export/DataDownload/get?_t={timestamp}' \
                      f'&page=1&size=2000&submitTimeBegin=&submitTimeEnd=&createdSysUser='
                      # f'&page=1&size=2000&submitTimeBegin=&submitTimeEnd=&createdSysUser=%E5%90%B4%E8%B4%A4%E6%96%87'
                resp = requests.get(url, headers=header)
                resp = resp.json()
                df = pd.DataFrame(resp['content'])
                df['taskStartTime'] = df['taskStartTime'].astype('datetime64[ns]')
                df_downfile = df[(df['taskStartTime'] > start_time) & (df['dataDownloadStatus'] == 'Success')&
                                 (df['clientIp'] == dfk.loc['ip','message'])][['downloadFile', 'dataSourceType', 'taskStartTime', 'dataDownloadStatus']].reset_index(drop=True)
                print(f"待下载的数据：{df[(df['taskStartTime'] > start_time)]}")
                if df_downfile.empty:
                    print(f"{start_time}后，ip:{dfk.loc['ip','message']}无可下载数据")
                    break
                else:
                    if df_downfile[df_downfile['dataDownloadStatus']=='Doing'].empty:
                        for i in range(len(df_downfile.index)):
                            if df_downfile.loc[i,'dataDownloadStatus'] =='Success':
                                download_dic[df_downfile.loc[i,'downloadFile']] = df_downfile.loc[i,'dataSourceType']
                            else:
                                dic_sourcetype = {1: '1s数据', 0: '30数据', 8: '高精度数据'}
                                if df_downfile.loc[i,'dataDownloadStatus'] =='Empty':
                                    print(f"{dic_sourcetype[df_downfile.loc[i,'dataSourceType']]}:'Empty'")
                                elif df_downfile.loc[i,'dataDownloadStatus'] =='Cancel':
                                    print(f"{dic_sourcetype[df_downfile.loc[i, 'dataSourceType']]}:'Cancel'")
                        break
                    else:
                        print('等待')
                        time.sleep(30)
            if not df_downfile.empty:
                print('数据下载中')
                for url1 in download_dic.keys():
                    response = requests.get(url1).content
                    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
                    _tmp_file.write(response)
                    zf = zipfile.ZipFile(_tmp_file, mode='r')
                    zf.extractall(save_path)
                print('数据下载完成..')
                return tell_me
        except Exception as e:
            print(f"数据下载报错：{str(e)}")
            if try_downloard_count >= 5:
                tell_me = '数据尝试下载失败5次'
                break
            else:
                try_downloard_count += 1
                print('网页连接失败，等待2min尝试重连')
                time.sleep(120)  # 等待两分钟

def concat_files():
    path_save = [r'./20240130/data/1/', r'./20240130/data/2/']
    total_df = pd.DataFrame([], columns=['VIN', '时间'])

    for p in path_save:
        for i in glob.glob(os.path.join(p, '*.csv')):
            vin_name = os.path.split(i)[1].split('.')[0]
            print(f"路径：{i}, {vin_name}")
            df = pd.read_csv(i)
            df = df.fillna('空白')

            df_sigle = pd.DataFrame()
            out_df = pd.DataFrame(index=[vin_name])

            # 条件： 电源档位：空白或1   0x0:无效;0x1:OFF档;0x2:ACC档;0x3:ON档;0x4-0x7:预留
            #       充电枪：空白或1  0x0:未连接;0x1:交流充电枪连接;0x2:直流充电枪连接;0x3:交流充电枪和直流充电枪同时连接;
            #       0x4:VTOL放电枪连接;0x5:OBC-CC连接;0x6:V2V充放电枪连接;0x7:V2V充放电枪半连接

            df_sigle = df[((df['充电枪连接状态_(344)'] == 0.0) & (df['电源档位_(12D)']==1))
               | ((df['电源档位_(12D)']=='空白') & (df['充电枪连接状态_(344)'] == '空白'))]

            # df = df[(df['电源档位_(12D)']=='空白') | (df['电源档位_(12D)']==1)]
            # df_sigle['时间'] = df[(df['充电枪连接状态_(344)'] == 0.0)
            #                      | (df['充电枪连接状态_(344)'] == '空白')]['时间']
            df_sigle['VIN'] = vin_name
            df_sigle['day'] = pd.DatetimeIndex(df_sigle['时间']).day
            # print(f"df_sigle['day']:{df_sigle['day']}, {type(df_sigle['day'])}")

            day = set(df_sigle['day'].drop_duplicates())
            all_hour_list = set([i for i in range(0, 24, 1)])
            print(f"所有时间段：{all_hour_list}")
            for d in day:
                print(f"d:{d}=============")
                ddf = pd.DataFrame()
                ddf = df_sigle[df_sigle['day']==d]  # 取这一天
                ddf['hour'] = pd.DatetimeIndex(ddf['时间']).hour
                # df_sigle['mins'] = pd.DatetimeIndex(df_sigle['时间']).minute

                hours = set(ddf['hour'].drop_duplicates())
                print(f"此车{d}: 用车时段：{hours}")
                # out_df[d] = list(all_hour_list)  # 默认这一天所有小时
                if len(hours) < 24:
                    blank_hours = all_hour_list.difference(hours)
                    print(f"此车空闲时间段：{blank_hours}")
                else:
                    blank_hours = '无'
                out_df[d] = ','.join(str(blank_hours))
                print(f'-----------{out_df}')
                # h = ','.join(str(blank_hours))
                # ddddd = pd.DataFrame([','.join(str(blank_hours))], columns=[day], index=[vin_name])
                # print(f"每一天的时段：{pd.DataFrame({d: h}, index=[vin_name])}")
                # print(f"每一天的时段：{pd.DataFrame({d: h}, index=[vin_name])}")
                # out_df = pd.DataFrame({vin_name: {d: {'空闲时段': blank_hours}}}, columns=['vin', '日期'])
                # 后面比较长的数据的时候，需要怎么匹配，17行怎么匹配24行
            # df_sigle['mins_s'] = df_sigle['mins'].shift(-1)
            # df_sigle['持续分钟'] = df_sigle['mins_s'] - df_sigle['mins']
            # tm = 0
            # mlist = []
            # df_sigle = df_sigle.fillna(0)
            # for j, i in df_sigle['持续分钟'].items():
            #     print(f"item:{int(i)}")
            #     i = int(i)
            #     if i == -59 or i == 1:   #('-59', '0', '1', '2', '-2'):
            #         mm = 1
            #         # df_sigle['持续分钟'] = mm
            #     elif i == -2 or i == 2:
            #         mm = 2
            #     elif i == 3 or i == -3:
            #         mm = 3
            #     else:
            #         mm = 0
            #     mlist.append(mm)
            #     # tm += mm
            # df_sigle['持续分钟_'] = mlist

            # df_sigle['持续分钟_'] = df_sigle.groupby(['VIN', 'day', 'hour']).agg({'持续分钟_': 'sum'})
            # t = df_sigle['mins_s'] - df_sigle['mins']
            # if t.any() <= 1:
            #     df_sigle['持续分钟'] = t
            # df_sigle['持续分钟'] =
                total_df = pd.concat([total_df, out_df], axis=0)
            # df_1 = df[df['充电枪连接状态_(344)']==0.0]
            # df_2 = df[df['电源档位_(12D)']==1]
            if not out_df.empty:
                print(f"分析的文件\n {out_df}")
                # print(f"合并的文件\n {total_df}")
                out_df.to_csv(fr'./20240130/output_6/{vin_name}.csv')
            else:
                print('空')
            break
    total_df.to_csv(r'./20240130/output_6/total.csv')

def analyse_all(save_path):
    data_path = Path(save_path).parent
    for d in Path(data_path).iterdir():
        if d.is_dir():
            dp = data_path / d
            print(f'子目录：{dp}')
        else:
            for f in d.rglob('.csv'):
                print(f"当前{d}下的文件{f}")



def analyse_total(save_path=None):
    path_save = [r'./20240130/data/1/', r'./20240130/data/2/']
    output = r'./20240130/output_8/'
    total_vins = 0
    hh_vins = 0
    vins_tup = set()
    total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))
    signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))

    for p in path_save:
        for i in glob.glob(os.path.join(p, '*.csv')):
            total_vins += 1
            vin_name = os.path.split(i)[1].split('.')[0]
            df = pd.read_csv(i)
            # df = df[((df['充电枪连接状态_(344)'] == 0.0) & (df['电源档位_(12D)'] == 1))]

            # df = df.fillna('空白')
            # day = pd.DatetimeIndex(df['时间']).day
            df['hour'] = pd.DatetimeIndex(df['时间']).hour
            # grouped = df.groupby(pd.DatetimeIndex(df['时间']).to_period('1H'), as_index=False)['时间'].size()
            # df = pd.DatetimeIndex(df['时间']).resample('30T').sum()
            # df_time = pd.DatetimeIndex(df['时间']).shift(freq='30M')
            # df['向后30M'] = pd.DatetimeIndex(df['时间']) + datetime.timedelta(minutes=30)
            # grouped['hour'] = grouped['时间'].hour
            all_hour_list = set([i for i in range(0, 24, 1)])
            hours = set(df['hour'].drop_duplicates())  # 用车段
            dh = all_hour_list.difference(hours)
            # hh_vins = 0
            if len(dh) > 0:
                print(f'第{total_vins}=={vin_name}缺少时间段：{dh}')  # 空闲时间段
                for hh in dh:
                    # print(f"记录当前时段：{hh}")
                    # hh_vins += 1
                    # vins_tup.add(vin_name)
                    # vins_dic = {hh: vins_tup}
                    # vin_cnt = {hh: hh_vins}
                    # signal_df.loc[hh:hh, 'vins'] = ','.join(vins_tup)
                    # def combine_ratio(row):
                    #     print(f'========{row}')
                    #     return vin_name.join(row.values.astype(str))
                    vins_tup = signal_df.loc[hh:hh, 'vins'].fillna(' ')
                    print(f"获取当前{hh}vin列表：{vins_tup.tolist()}")
                    vins_tup = vins_tup + ',' + vin_name
                    # vins_tup = vins_tup.add(vin_name)
                    print(f"====添加后的{hh}vin列表：{vins_tup}")

                    signal_df.loc[hh:hh, 'vins'] = vins_tup
                    cnt = len(vins_tup.tolist()[0].split(','))
                    # cnt = len(signal_df.loc[hh:hh, 'vins'])
                    print(f'cnt:{cnt}')
                    signal_df.loc[hh:hh, '车辆数'] = cnt

                    # print(vin_cnt, vins_dic)
                    # print(f"单车:{signal_df}")
                    signal_df.to_csv(fr'./{output}/{vin_name}.csv')
            else:
                print(f'第{total_vins}:{vin_name}全段：{hours}')
            # if total_vins >= 15:
            #     break
        # print(vins_dic, vin_cnt)

        # break
    # for hh, vv in vins_dic.items():
    #     total_df['vins'] = total_df.loc[hh:, vv]
    #
    # for hh, vv in vin_cnt.items():
    #     total_df['车辆数'] = total_df.loc[hh:, vv]
    #         # print(f"grouped=====\n{signal_df}")
    #         # break
    print(f'总车辆数：{total_vins}')
    signal_df.to_csv(fr'./{output}/total.csv')

def analyse_total_2(save_path=None):
    path_save = [r'./20240130/data/1/', r'./20240130/data/2/']
    output = r'./20240130/output_9/'
    total_vins = 0
    hh_vins = 0
    vins_tup = set()
    total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))
    signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))

    for p in path_save:
        for i in glob.glob(os.path.join(p, '*.csv')):
            total_vins += 1
            vin_name = os.path.split(i)[1].split('.')[0]
            df = pd.read_csv(i)
            df = df[((df['充电枪连接状态_(344)'] == 0.0) & (df['电源档位_(12D)'] == 1))]

            # df = df.fillna('空白')
            # day = pd.DatetimeIndex(df['时间']).day
            df['hour'] = pd.DatetimeIndex(df['时间']).hour
            # grouped = df.groupby(pd.DatetimeIndex(df['时间']).to_period('1H'), as_index=False)['时间'].size()
            # df = pd.DatetimeIndex(df['时间']).resample('30T').sum()
            # df_time = pd.DatetimeIndex(df['时间']).shift(freq='30M')
            # df['向后30M'] = pd.DatetimeIndex(df['时间']) + datetime.timedelta(minutes=30)
            # grouped['hour'] = grouped['时间'].hour
            all_hour_list = set([i for i in range(0, 24, 1)])
            hours = set(df['hour'].drop_duplicates())  # 用车段
            dh = all_hour_list.difference(hours)
            # hh_vins = 0
            if len(dh) > 0:
                print(f'第{total_vins}=={vin_name}缺少时间段：{dh}')  # 空闲时间段
                for hh in dh:
                    # print(f"记录当前时段：{hh}")
                    # hh_vins += 1
                    # vins_tup.add(vin_name)
                    # vins_dic = {hh: vins_tup}
                    # vin_cnt = {hh: hh_vins}
                    # signal_df.loc[hh:hh, 'vins'] = ','.join(vins_tup)
                    # def combine_ratio(row):
                    #     print(f'========{row}')
                    #     return vin_name.join(row.values.astype(str))
                    vins_tup = signal_df.loc[hh:hh, 'vins'].fillna(' ')
                    print(f"获取当前{hh}vin列表：{vins_tup.tolist()}")
                    vins_tup = vins_tup + ',' + vin_name
                    # vins_tup = vins_tup.add(vin_name)
                    print(f"====添加后的{hh}vin列表：{vins_tup}")

                    signal_df.loc[hh:hh, 'vins'] = vins_tup
                    cnt = len(vins_tup.tolist()[0].split(','))
                    # cnt = len(signal_df.loc[hh:hh, 'vins'])
                    print(f'cnt:{cnt}')
                    signal_df.loc[hh:hh, '车辆数'] = cnt

                    # print(vin_cnt, vins_dic)
                    # print(f"单车:{signal_df}")
                    signal_df.to_csv(fr'./{output}/{vin_name}.csv')
            else:
                print(f'第{total_vins}:{vin_name}全段：{hours}')
            # if total_vins >= 15:
            #     break
        # print(vins_dic, vin_cnt)

        # break
    # for hh, vv in vins_dic.items():
    #     total_df['vins'] = total_df.loc[hh:, vv]
    #
    # for hh, vv in vin_cnt.items():
    #     total_df['车辆数'] = total_df.loc[hh:, vv]
    #         # print(f"grouped=====\n{signal_df}")
    #         # break
    print(f'总车辆数：{total_vins}')
    signal_df.to_csv(fr'./{output}/total.csv')

def analyse_total_3(save_path):
    """
    需求：看仰望指定车辆（529辆车）哪些时段符合OTA升级条件。
    升级条件：
    条件1有数据情况：
    case1:车辆电源档位处于off档 + 没有插枪充电；
    case2:车辆电源档位处于off档 + 充电空；
    case3:车辆电源档位空 + 没有插枪充电；
    case4:车辆电源档位空 + 充电空；
    条件2没数据情况：车辆处于休眠，完全没有报文数据：
    case1:没有数据时的时间标记点往前推{x=3分钟}，如果满足条件1的case1,则可以更加充分的判定为真休眠；
    case2:不满足条件2-case1的都不能算在真休眠里，即不满足条件2。
    隐含信息：因为是批量推送，所有要看所有车的一个整体统计信息，不是每一辆车；
            不能只看一两天，要多观察几天，推断规律。包含周内和周末数据最好。
    目标结果：条件1与条件2并集，输出符合的时段、车辆明细、占比
    针对条件2的分析方法：30秒的数据，正常是每辆车都有数据，如果一段时间休眠了那么这段时间就没有数据，则说明车辆休眠了，输出没有数据的vin号和休眠时间段。
    1. 如何找到休眠时间段呢？构建全频率比较高的时间序列，作为参考时间序列。源数据时间与参考序列比较，找到差值，即缺失值。
    2. 构建参考时间序列：开始时间取源数据时间的最小值，结束时间取源数据的最大值，频率取间隔时间段，比如想找到30分钟的缺失值，则频率取30分钟，
        这样就构建了一个没30分钟没有缺失的时间序列。这里的话有不同的分析方法；
    第一种方法：将源数据的时间列按照规定时间段分组，分组后有空值和缺失值按照步骤3进行处理。两种方法的不同点：方法一不用对源数据重新采用，只需要生成一个全时间的参考时间序列，
    然后从分组后的数据与全时间序列作差集，就可以找到空的时间段。
    第二种方法：将源数据的时间列重新下采样，如果下采样有空值和缺失值，也按照步骤3进行处理。
    3. 条件2源数据处理：
        （1）增加vin到合并数据的列中
        （2）截取时间到分钟，形成时间格式2024-01-26 12:25的时间列，数据框：时间，vin
        （3）按照每30分钟聚合数据：重复数据处理：同一分钟内有很多车辆重复，同时一辆车本身也有重复，拼接（vin+1），并统计vin数；
        空值处理：说明全部车辆都休眠了。不用填充。
        （4）因此，只能是输出不为空的时段，然后从全时段取反。
        （5）预期输出结果：{频率}时段，用车vin，用车车辆数，休眠vin，休眠车辆数，休眠vin占比%
                        12：00, vin1,vin2，count(), 取差集，count(), 休眠车辆数/total_vin_cnt*100
                        12：30, vin1,vin3，取差集（反，补集）
                        13：00, vin2,vin2，取差集（反，补集）
                        13：30, vin4,vin3，取差集（反，补集）
                        14：30, nan, 全集
        （6）全休眠时段(标记点)的前{x}分钟的电源off档，和没充电数据筛选。去源数据里选择时间段>=标记点-{x}和<标记点的vin，表示才是真的休眠，否则不能添加到
            休眠的vin里，应该添加到用车车辆数。及从标记是的里，反操作。

    :param save_path:下载原始原始存放路径
    :return:
    函数功能：采用分组时间列的方法，先不用重采用的方法。
    """
    # 文件夹名称
    save_path = f"./{str(datetime.date.today() - datetime.timedelta(days=5))}/data/"
    os.path.exists(save_path) or os.makedirs(save_path)
    # 判断有没有输出路径，没有则新建
    output_path = f"./{str(datetime.date.today())}/output"
    os.path.exists(output_path) or os.makedirs(output_path)
    # output = r'./20240130/output_9/'
    total_vins = 0
    hh_vins = 0
    vins_tup = set()
    total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))
    signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0,24,1))
    # for i in Path(save_path).iterdir():
    #     print(f'查找子目录：{i}')
        # print(f'for 循环执行完成或完全没有匹配到条件')
    df_list = []
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        total_vins += 1
        df = pd.read_csv(p)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        df = df.drop(columns=df.columns[[3]], axis=1)   # 按照列号删除，非常重要

        df['vin'] = p.stem
        # print(f"单文件信息：{df}")

        df_list.append(df)
        if total_vins >= 5:
            break
    # 合并所有df, 并指定数据类型
    df_total = pd.concat(df_list, ignore_index=False)
    return df_total
    # df_total.rename({'': '充电枪'})
    # origin_tt_path = f"{output_path}\\total_original.csv"
    # print(origin_tt_path)  # 作为整体字符串拼接的话，直接用+比较直接；如果是把一个序列按照一定分割拼接，用"seporator".join(sequence)
    # df_total.to_excel(origin_tt_path, engine='openpyxl')
    # df_total.to_csv(origin_tt_path)
    # 按照列名删除多余的列，[[col1]], [[col1,col2,col3]]
    # new_df = df_total.drop(columns=['col1'])
    # print(new_df.head())
    # 按照列号删除多余的列，[[3]], [[3,4,5]], 也可以原位删除，inplace=True
    # new_df = df_total.drop(df_total.columns[[3]], axis=1).fillna(-1)
    # print(f'new_df: \n {len(new_df.index)}')
    # new_df = new_df.astype({'充电枪连接状态_(344)': int, '电源档位_(12D)': int})   # 选择1,2列并转换数据类型，返回没有其他列
    # print(f'{new_df.dtypes}')  #查看多列数据类型，默认数
    # print(f'{new_df.head()}')
    # 值类型是float64
    # new_df.iloc[:,[1]]= 充电枪连接状态_(344),new_df.iloc[:,[2]]=电源档位_(12D)
    # 注意：new_df.iloc[:,1]用下标索引一列的时候，不能写成[[1]]。一列满足多个值条件筛选，isin()函数。
    # condition_1: 充电枪没有连接且下电， 充电抢没连接且挡位为空，和充电抢数据为空且下电，和充电抢和挡位数据都为空
    # condition_1 = new_df[(new_df.iloc[:,1].isin([0.0,-1])) & (new_df.iloc[:,2].isin([1.0,-1]))]
    # print(condition_1.head())
    # condition_2: 时间断层，时间间隔大于等于30分钟且断层前3分种内是OFF档+整车功能无需求
    # df_dtidx = pd.DatetimeIndex(new_df.iloc[:,1])
    # print(df_dtidx)
    # 对日期索引异常值处理，1970，1969年
    # 移动一步等于30秒，现在需要往后移动30分钟，一共30*60秒，因此=30*60/30=60步
    # condition_2 = new_df.shift(60)   #整体平移
    # condition_2 = new_df.shift(60)   #按照分钟平移
    # condition_2 = pd.Timestamp(new_df['时间']).shift(60)
    # min_dt = new_df['时间'].min()
    # print(f"min_dt:{min_dt}")

    # max_dt = new_df['时间'].max()
    # print(f"max_dt:{max_dt}")
    # print(f"{df_total.columns}======列名")
    # 向下采样: 采样频率更低，向上采样：采样频率更高；参考全的时间序列
    idx = pd.period_range(start=df_total['时间'].min(), end=df_total['时间'].max(), freq='30T')
    # 这个idx没有重复值
    print(f"idx:{idx}")
    pindex = pd.PeriodIndex(data=df_total['时间'], freq='30T')
    # df_total['pindex'] = pindex
    # print(f"能设置成功吗：{df_total} \n 可以设置成功")

    # pindex 有重复值
    # 因此要么是增加一列，时间就是idx; 这样的话其实就是重采样;或是是把时间列设置为datatimeindex
    # grouped = df_total.groupby(df_total['pindex'])       # 不能用不同长度的数据进行groupby
    # grouped = df_total.groupby(idx)       # 不能用不同长度的数据进行groupby
    # TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'Index'
    # 重采样的前提就是类型转换，和reset_index差不多
    def combine_section(row):
        print(f'========{row}')
        return ','.join(row.values.astype(str))
    # print(f"grouped:{grouped.transform(lambda row: combine_section(row))}")
        # 对分组后的数据进行拼接，combine_secton是ok的，但却是一行行处理，效率比较低，不是按照二维数据处理，是处理的一维数据。
    # print(f"grouped:{grouped}")
    # print(f"grouped:{grouped['pindex']}")
    # print(f"分组求平均值========\n:{grouped.mean}")
    # print(f"grouped:{grouped['充电枪连接状态_(344)'].count()}")
    # df_total.set_index('pindex', inplace=True)  # 居然设置索引是可以允许有重复值的
    # print(f"index:{df_total.index}")
    # print(f"df_total:{df_total}")
    # 将多列表头换成一列表头
    # print(f"df_total:{df_total.resample('30T').count()}")
    #
    # print(f"显示index有空的:{df_total.resample('30T').index.isna()}")
    # AttributeError: 'PeriodIndexResampler' object has no attribute 'index'
    # 如何取出resample后的某一列数据
    # print(f"30T对数值求和:{df_total.resample('30T', label='left', closed='left').sum()}")
    # print(f"30T对数值求和:{df_total.resample('30T', label='left', closed='left').asfreq()}")
    # print(f"显示vin有重复的:{df_total.resample('30T').duplicatied()}")
    # print(f"连接vin有重复的:{df_total.resample('30T').str.cat(',')}")

    # 两个列表的差集
        # .apply({'vin': lambda row: ','.join(row), total_df.columns[[1]]: 'count'})
    # ValueError: cannot reindex on an axis with duplicate labels
    # print(f"new_df:{new_df[new_df.index.duplicated()]}")
    # 定位查看重复的数据2024-01-30 10:22:39, 如何查看某个值
    # print(f"new_df:{new_df.loc['2024-01-30 10:22:39']}")

    # 通过取反去重
    # print(f"new_df 取反:{new_df[~new_df.index.duplicated()]}")
    # condition_2 = pd.Series(new_df[~new_df.index.duplicated()]['时间'], index=idx)
    # print(f"condition_2 取反 :{condition_2}")
    # print(f"condition_2 取反 :{condition_2.isna().count()}")


    # period_range 不能统计出缺失数据
    # 按照指定时长分组统计数据条数
    # print(f"condition_2:{condition_2['时间'].resample('30T').sum()}")
    # print(f"condition_2:{condition_2.value_counts()}")

    # condition_2['时间'].resample()
    # 移动后统计某一列NaN的个数
    # print(f"condition_2:{condition_2['时间'].isna().count()}")


def anslyse_0204():
    save_path = f"./{str(datetime.date.today() - datetime.timedelta(days=0))}/data/"
    os.path.exists(save_path) or os.makedirs(save_path)
    # 判断有没有输出路径，没有则新建
    output_path = f"./{str(datetime.date.today())}/output"
    os.path.exists(output_path) or os.makedirs(output_path)
    # output = r'./20240130/output_9/'
    total_vins = 0
    hh_vins = 0
    vins_tup = set()
    total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    # for i in Path(save_path).iterdir():
    #     print(f'查找子目录：{i}')
    # print(f'for 循环执行完成或完全没有匹配到条件')
    df_list = []
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        total_vins += 1
        df = pd.read_csv(p)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要

        df['vin'] = p.stem
        # print(f"单文件信息：{df}")

        df_list.append(df)
        if total_vins >= 5:
            break
    # 合并所有df, 并指定数据类型
    df_total = pd.concat(df_list, ignore_index=False)
def anslyse_0206():
    save_path = f"./{str(datetime.date.today() - datetime.timedelta(days=0))}/data/"
    os.path.exists(save_path) or os.makedirs(save_path)
    # 判断有没有输出路径，没有则新建
    output_path = f"./{str(datetime.date.today())}/output"
    os.path.exists(output_path) or os.makedirs(output_path)
    # output = r'./20240130/output_9/'
    total_vins = 0
    hh_vins = 0
    vins_tup = set()
    total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    # for i in Path(save_path).iterdir():
    #     print(f'查找子目录：{i}')
    # print(f'for 循环执行完成或完全没有匹配到条件')
    df_list = []
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        total_vins += 1
        df = pd.read_csv(p)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        # df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要

        df['vin'] = p.stem
        # print(f"单文件信息：{df}")

        df_list.append(df)
        if total_vins >= 5:
            break
    # 合并所有df, 并指定数据类型
    df_total = pd.concat(df_list, ignore_index=False)
    # print(df_total[df_total.columns[[1]]!=3.0])

def concat_all_data():
    save_path = f"./数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode"
    os.path.exists(save_path) or os.makedirs(save_path)
    # 判断有没有输出路径，没有则新建

    output_path = f"./数据存储/{str(datetime.date.today())}/output"
    os.path.exists(output_path) or os.makedirs(output_path)
    total_vins = 0
    vins_tup = set()
    # total_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    # signal_df = pd.DataFrame([], columns=['vins', '车辆数', '占比'], index=range(0, 24, 1))
    # for i in Path(save_path).iterdir():
    #     print(f'查找子目录：{i}')
    # print(f'for 循环执行完成或完全没有匹配到条件')
    df_list = []
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        print(f"当前读取文件：{p}")
        #跳过加密文件
        total_vins += 1
        df = pd.read_csv(p, low_memory=False)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        # df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要

        df['vin'] = p.stem
        # print(f"单文件信息：{df}")

        df_list.append(df)
        # if total_vins >= 5:
        #     break
    # 合并所有df, 并指定数据类型
    global df_total
    df_total = pd.concat(df_list, ignore_index=True)
    # print(df_total[df_total.columns[[1]]!=3.0])
    df_total.to_csv(f'{output_path}/contact.csv')


def anslyse_0226(df):
    """
    分析任务：仰望U8，从4064台车筛选近3天凌晨0点~6点处于off档的车辆
    生成时间段，半个小时为时间分割区间00:00~00:30，00:30~10:00。。。。。。05:00~05:30，05:30~06:00
    df['充电枪连接状态_(344)']!=0
充电枪连接状态_(344)	3			0x0:未连接;0x1:交流充电枪连接;0x2:直流充电枪连接;0x3:交流充电枪和直流充电枪同时连接;0x4:VTOL放电枪连接;0x5:OBC-CC连接;0x6:V2V充放电枪连接;0x7:V2V充放电枪半连接
电源档位_(12D)	3	7	0	0x0:无效;0x1:OFF档;0x2:ACC档;0x3:ON档;0x4-0x7:预留
    :param df: df_total, 全局变量，已经将所有的文件合并到一起，并且添加了vin
    小时：df['时间'].str[11:13]
    分钟：df['时间'].str[14:16], 因此小时：分钟表示为：df['时间'].str[11:16]
    左开右闭区间，（时间>=00:00 & 时间<00:30）.empty or
                if 判断是否为空，如果为空，则输出此时间段的vin
                else 不为空，
                    if  (df['电源档位_(12D)']!=3)（off档）
                        追加vin
                    else
                        不满足添加，pass
    :return:
    """
    print(df.dtypes)  # object类型
    df['时间'].astype(str)
    # 不解析是默认浮点数据，比如电源档位_(12D) == 1.0
    # df = df[(df['时间'].str[11:13] >='07') & (df['时间'].str[11:13]<'08') & (df['电源档位_(12D)']==1.0)]
    # 注意时间断层的时候是筛选不出数据的。
    # all_hour_list = set([i for i in range(0, 6,  0.5)])  # 步长不能为小数  30s数据是float，高精度是int64
    # df = df[(df['时间'].str[11:16] >= '00:00') & (df['时间'].str[11:16] <= '06:00') & (df['电源档位_(12D)']!=3)]  #['时间'].str[11:16]
    df = df[(df['时间'].str[11:16] >= '00:00') & (df['时间'].str[11:16] <= '06:00') &
            (df['电源档位_(12D)']!=3.0) & (df['充电枪连接状态_(344)']==1.0)]  #['时间'].str[11:16]
    # df['时间点'] = pd.to_datetime(df['时间'].str[0:16], format="%Y-%m-%d %H:%M")
    if df.empty:  # 0~6点on档 全部为空，一条数据都没有
        # 全部都是满足空闲条件的，应该添加默认的时间段和vin
        idx = pd.date_range(start='1900-01-01 00:00', end='1900-01-01 06:00', freq='30T')
        # print(f"日期范围索引：{idx}")
        df = df.reindex(idx)  # 主要，如果df本身是empty，不能调用df.set_index(idx)函数，会报行数不匹配错误;但是reindex函数需要重新赋值
        # print(f"日期范围索引df：{df}")
    else:
        # print(f"on档时间段：\n{pd.to_datetime(df[df['电源档位_(12D)']==3]['时间'], format='30T')}")  # 这样format会报错
        # df['日期'] = pd.to_datetime(df['时间'].str[:10])  # 只要小时和分钟，会自动填充日期为1990-01-01

        df['时间点'] = pd.to_datetime(df['时间'].str[11:16], format="%H:%M")
        df.set_index('时间点', inplace=True)
        df = df.resample('30T').agg({'vin': lambda row: ','.join(row)})
    # df['vin'].drop_duplicates(inplace=True)
    # df.reset_index(drop=False, inplace=True)
    # df['时间点'].astype(str)
    # df['时间段'] = df['时间点'].str[11:16]
    # df.drop(['时间点'], axis=1, inplace=True)
    output_path = f"./数据存储/{str(datetime.date.today())}/output"
    os.path.exists(output_path) or os.makedirs(output_path)
    df.to_csv(f'{output_path}/result.csv')
    # vins_out_list = []
    # if df.empty:
    #     vins_out_list = df['vin'].to_list()
    # else:
    #     if not df[df['电源档位_(12D)']!=3].empty:
    #         vins_out_list = df['vin'].to_list()
    #     else:
    #         pass
    #
    # print(vins_out_list)

def demo02(df):
    """
    分析秦PD4.00.02OTA升级结果明细.xlsx，车辆是否报故障
    :param df:
    :return:
    """
    # 多个文件处理，且分批处理，因为输出结果超超过excel单元格最大宽度了
    import os
    from pathlib import Path
    # path = r'..\00-bd-monitor\数据存储\2024-02-27\data\High_Precision(R)_8\LGXEK1C4XP0583078.csv'
    save_path = f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode/"
    # os.path.exists(save_path) or os.makedirs(save_path)
    df_list = []
    total_vins = 0
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        print(f"当前读取文件：{p}")
        # 跳过加密文件
        total_vins += 1

        df = pd.read_csv(p, low_memory=False)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        # df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要
        # print(f"分析字段类型：{df['车辆当前故障1_(387)'].dtypes}")


        df = df[(df['车辆当前故障1_(387)']!=0) | (df['车辆当前故障2_(387)']!=0) | (df['车辆当前故障3_(387)']!=0)]
        # print(f"0~6点on档：\n{df}")
        if df.empty:  # 0~6点on档 全部为空，一条数据都没有
            continue
            # 全部都是满足空闲条件的，应该添加默认的时间段和vin
            idx = pd.date_range(start='1900-01-01 00:00', end='1900-01-01 06:00', freq='30T')
            # print(f"日期范围索引：{idx}")
            df = df.reindex(idx)  # 主要，如果df本身是empty，不能调用df.set_index(idx)函数，会报行数不匹配错误;但是reindex函数需要重新赋值
            # print(f"日期范围索引df：{df}")
        else:
            # print(f"on档时间段：\n{pd.to_datetime(df[df['电源档位_(12D)']==3]['时间'], format='30T')}")  # 这样format会报错
            df['日期'] = pd.to_datetime(df['时间'].str[:10])  # 只要小时和分钟，会自动填充日期为1990-01-01

        df['vin'] = p.stem
        # df.drop(columns=['电源档位_(12D)', '时间'], inplace=True)
        df.drop(columns='时间', inplace=True)
        # df['时间段'] = df_idx.str[11:16]
        # print(f"on档补集添加vin：\n{df}")  # 补集后面要加括号
        df_list.append(df)

        # if total_vins <= 2:
        #     break
        # else:
        #     continue
    if not df_list:
        df_total = pd.concat(df_list, ignore_index=True)
        df_group = df_total.groupby(['vin', '日期', ]).mean()
        # df_total.set_index(['时间', 'vin'])
        print(f"分组后的数据：{df_group}")
        df_group = df_group.reset_index(drop=False)
        # 计算车辆数：excel中=LEN(C2)-LEN(SUBSTITUTE(C2,",",""))+1
        # df_group['车辆数'] = df_group['vin']
        print(f"分组reset_index的数据：{df_group}")
        # 如何排序
        df_group.sort_values(by=['vin', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
        df_group.to_csv(f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/output/total.csv", index=False)
    else:
        print('没有符合要求的数据。')

def demo01(df):
    """
    单个文件-分析仰望车辆OTA升级预判
    :param df:
    :return:
    """
    # 多个文件处理，且分批处理，因为输出结果超超过excel单元格最大宽度了
    import os
    from pathlib import Path
    # path = r'..\00-bd-monitor\数据存储\2024-02-27\data\High_Precision(R)_8\LGXEK1C4XP0583078.csv'
    save_path = f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode/"
    # os.path.exists(save_path) or os.makedirs(save_path)
    df_list = []
    total_vins = 0
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        print(f"当前读取文件：{p}")
        # 跳过加密文件
        total_vins += 1

        df = pd.read_csv(p, low_memory=False)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        # df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要
        # print(f"分析字段类型：{df['车辆当前故障1_(387)'].dtypes}")
        # 充电枪连接状态_(344)  =0是未连接
        # 电源档位 = 3是on档

        #  满足业务条件的选择
        print(f"分析数据类型：\n{df.dtypes}")

        df = df[((df['时间'].str[11:16] >= '00:00') & (df['时间'].str[11:16] <= '06:00')) &
                ((df['电源档位_(12D)'] != 3.0) & (df['充电枪连接状态_(344)'] == 0.0))]  # ['时间'].str[11:16]

        # df = df[(df['充电枪连接状态_(344)']!=0) | (df['电源档位_(12D)']!=0) | (df['车辆当前故障3_(387)']!=0)]
        print(f"0~6点OFF档和充电枪未连接：\n{df}")
        if df.empty:  # 0~6点on档 全部为空，一条数据都没有
            # continue
            # 全部都是满足空闲条件的，应该添加默认的时间段和vin
            idx = pd.date_range(start='1900-01-01 00:00', end='1900-01-01 06:00', freq='30T')
            # print(f"日期范围索引：{idx}")
            df = df.reindex(idx)  # 主要，如果df本身是empty，不能调用df.set_index(idx)函数，会报行数不匹配错误;但是reindex函数需要重新赋值
            # print(f"日期范围索引df：{df}")
        else:
            # print(f"on档时间段：\n{pd.to_datetime(df[df['电源档位_(12D)']==3]['时间'], format='30T')}")  # 这样format会报错
            # df['日期'] = pd.to_datetime(df['时间'].str[:10])  # 只要小时和分钟，会自动填充日期为1990-01-01
            df['时间点'] = pd.to_datetime(df['时间'].str[11:16], format="%H:%M")
            df.set_index('时间点', inplace=True)
        df['vin'] = p.stem
        # df.drop(columns=['电源档位_(12D)', '时间'], inplace=True)
        df.drop(columns='时间', inplace=True)
        df = df.resample('30T').agg({'vin': lambda row: ','.join(row)})

        # df['时间段'] = df_idx.str[11:16]
        # print(f"on档补集添加vin：\n{df}")  # 补集后面要加括号
        df_list.append(df)
        print(f"为什么df_list是空的：{df_list}")
        # if total_vins <= 2:
        #     break
        # else:
        #     continue
    if df_list:  # 列表判断是否为空
        df_total = pd.concat(df_list, ignore_index=True)
        df_group = df_total.groupby(['vin', '日期', ]).mean()
        # df_total.set_index(['时间', 'vin'])
        print(f"分组后的数据：{df_group}")
        df_group = df_group.reset_index(drop=False)
        # 计算车辆数：excel中=LEN(C2)-LEN(SUBSTITUTE(C2,",",""))+1
        # df_group['车辆数'] = df_group['vin']
        print(f"分组reset_index的数据：{df_group}")
        # 如何排序
        df_group.sort_values(by=['vin', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
        df_group.to_csv(f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/output/total.csv", index=False)
    else:
        print('没有符合要求的数据。')

def demo_more(df):
    """
    多个个文件-分析仰望车辆OTA升级预判
    :param df:
    :return:
    """
    # 多个文件处理，且分批处理，因为输出结果超超过excel单元格最大宽度了
    import os
    from pathlib import Path
    # path = r'..\00-bd-monitor\数据存储\2024-02-27\data\High_Precision(R)_8\LGXEK1C4XP0583078.csv'
    save_path = f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode/"
    df_list = []
    total_vins = 0
    for p in Path(save_path).glob('**/*.csv'):  # 查找save_path指定目录以及子目录下所有csv文件，且不访问父目录
        print(f"当前读取文件：{p}")
        # 跳过加密文件
        total_vins += 1

        df = pd.read_csv(p, low_memory=False)
        # 把文件名作为一列vin数据，pandas读取文件的时候，获取文件属性文件名的方法。
        # 如果按照暴力方法，就是直接取倒数的的[5,5+17]
        # 正常的方法有，按照path类取文件名，不包含后缀；或者是按照文件的固有属性，取文件名的方法。
        # print(f"单文件信息：{p.stem}, {p.name}") p.stem不带后缀名的，p.name是包含后缀名的
        # df = df.drop(columns=df.columns[[3]], axis=1)  # 按照列号删除，非常重要
        # print(f"分析字段类型：{df['车辆当前故障1_(387)'].dtypes}")
        # 充电枪连接状态_(344)  =0是未连接
        # 电源档位 = 3是on档

        #  满足业务条件的选择
        print(f"分析数据类型：\n{df.dtypes}")

        all_cols = df.columns
        save_cols = ['时间']  # 保留的列
        del_cols = all_cols.difference(save_cols)  # 待删除的列

        df = df[((df['时间'].str[11:16] >= '00:00') & (df['时间'].str[11:16] <= '06:00')) &
                ((df['电源档位_(12D)'] == 3.0) |
                 (df['充电枪连接状态_(344)'].isin([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])))]
        print(f"on档或者充电枪连接：\n{df}")
        if df.empty:
            # 全部都是满足空闲条件的，应该添加默认的时间段和vin
            idx = pd.date_range(start='1900-01-01 00:00', end='1900-01-01 06:00', freq='30T')
            print(f"日期范围索引：{idx}")  # 如何给索引命名
            df = df.reindex(idx)  # 主要，如果df本身是empty，不能调用df.set_index(idx)函数，会报行数不匹配错误;但是reindex函数需要重新赋值
            df.index.name = '时间段'
            print(f"添加全时间段时间索引后的索引：{df}")  # 如何给索引命名
            # df.index.name = 'y'  # 方法一
            # df.index.names = ['y']  # 方法二
            # df.index.set_names = 'y'  # 方法三
            # df.index.set_names = ['y']  # 方法三
            #
            # df

            # df.rename(index={"index": "时间段"}, inplace=True)
            # print(f"日期范围索引df：{df}")
        else:
            df['时间段'] = pd.to_datetime(df['时间'].str[11:16], format="%H:%M")  # 只要小时和分钟，会自动填充日期为1990-01-01
            df.set_index('时间段', inplace=True)
            df = df.resample('30T').first()
            print(f"去重取第一条：\n{df}")
            df_idx = df.index
            print(f"去重取第一条df_idx：\n{df_idx}")
            idx = pd.date_range(start='1900-01-01 00:00', end='1900-01-01 06:00', freq='30T')

            idx_diff = idx.difference(df_idx)
            print(f"索引差集：{idx_diff}")
            df = df.reindex(idx_diff)
            df.index.name = '时间段'
            print(f"重新索引后df：{df}")
            # print(f"on档：\n{df[df['电源档位_(12D)']==3]}")  # 注意这样的输出是没有时间断层的数据的。不包含空值
            # df = df[~(df['电源档位_(12D)']==3)]
            # print(f"on档补集：\n{df}")  # 补集后面要加括号
        # df_idx = df.index.astype(str)
        # print(f"将索引改为字符串并截取小时分钟：{df_idx.str[11:16]}")
        df['vin'] = p.stem
        df.drop(columns=['时间', '电源档位_(12D)', '充电枪连接状态_(344)'], inplace=True)
        # df.drop(columns='时间', inplace=True)
        # df = df.resample('30T').agg({'vin': lambda row: ','.join(row)})

        # df['时间段'] = df_idx.str[11:16]
        # print(f"on档补集添加vin：\n{df}")  # 补集后面要加括号
        df_list.append(df)
        # if total_vins <= 2:
        #     break
        # else:
        #     continue
    if df_list:  # 列表判断是否为空
        df_total = pd.concat(df_list, ignore_index=False)  # ignore_index如果设置成 Flase, 会默认第一列为索引列
        print(f"合并后数据列：{df_total.columns}, 索引：{df.index}")

        # df_group = df_total.groupby(['vin', '时间段']).mean()
        df_group = df_total.groupby(['时间段', 'vin']).mean()
        # df_total.set_index(['时间', 'vin'])
        print(f"分组后的数据：{df_group}")  # 当字段都作为分组时，剩余没有字段，则df_group 数据是空，但实际索引是有值的
        # 分组后的数据：Empty DataFrame
        # Columns: []
        # Index: [(LGXEK1C49P0803147, 1900-01-01 01:00:00), (LGXEK1C49P0803147, 1900-01-01 01:30:00), (LGXEK1C49P0803147, 1900-01-01 02:00:00), (LGXEK1C49P0803147, 1900-01-01 02:30:00), (LGXEK1C49P0803147, 1900-01-01 03:00:00), (LGXEK1C49P0803147, 1900-01-01 03:30:00), (LGXEK1C49P0803147, 1900-01-01 04:00:00), (LGXEK1C49P0803147, 1900-01-01 04:30:00), (LGXEK1C49P0803147, 1900-01-01 05:00:00), (LGXEK1C49P0803147, 1900-01-01 05:30:00), (LGXEK1C49P0803147, 1900-01-01 06:00:00)]
        df_group = df_group.reset_index(drop=False)
        # 重新根据索引命名时间段名字
        df_group['时间段'] = df_group['时间段'].astype(str)
        df_group['时间段'] = df_group['时间段'].str[11:16]
        # 计算车辆数：excel中=LEN(C2)-LEN(SUBSTITUTE(C2,",",""))+1
        # df_group['车辆数'] = df_group['vin']
        print(f"分组reset_index的数据：{df_group}")
        # 如何排序
        # df_group.sort_values(by=['vin', '时间段'], ascending=[False, True], ignore_index=True, inplace=True)
        df_group.sort_values(by=['时间段', 'vin'], ascending=[True, True], ignore_index=True, inplace=True)
        # df_group.sort_values(by=['vin'], ascending=[False], ignore_index=True, inplace=True)
        df_group.to_csv(f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/output/total.csv", index=False)
    else:
        print('没有符合要求的数据。')

def demo_single(df):
    # 单个文件处理
    save_path = f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode/LGXEK1C40P0728175.csv"
    # save_path = f"../00-bd-monitor/数据存储/{str(datetime.date.today() - datetime.timedelta(days=0))}/decode/AllVin_王喻梅_20240305094827_keep.csv+ (多个连接)_AllVin_王喻梅_20240305094827_keep.csv"

    # path = r'..\00-bd-monitor\数据存储\2024-02-27\data\High_Precision(R)_8\LGXEK1C4XP0583078.csv'
    df = pd.read_csv(save_path)
    # 处理单个文件,从源头减少数据，只保留0点到6点的数据，在数据处理的时候要看是否结果为空。
    # df = df[(df['时间'].str[11:13] >='00') & (df['时间'].str[11:13]<'06') & (df['电源档位_(12D)']==3)]
    df = df[((df['时间'].str[11:16] >= '00:00') & (df['时间'].str[11:16] <= '06:00')) &
            ((df['电源档位_(12D)'] == 3.0) | (df['充电枪连接状态_(344)'].isin([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])))]
    print(f"on档或者充电枪连接：\n{df}")
    if df.empty:
        # 全部都是满足空闲条件的，应该添加默认的时间段和vin
        idx = pd.date_range(start='00:00', end='06:00', freq='30T')
        print(f"日期范围索引：{idx}")
        df = df.reindex(idx)  # 主要，如果df本身是empty，不能调用df.set_index(idx)函数，会报行数不匹配错误;但是reindex函数需要重新赋值
        print(f"日期范围索引df：{df}")
    else:
        # print(f"on档时间段：\n{pd.to_datetime(df[df['电源档位_(12D)']==3]['时间'], format='30T')}")  # 这样format会报错
        df['时间点'] = pd.to_datetime(df['时间'].str[11:16], format="%H:%M")  # 只要小时和分钟，会自动填充日期为1990-01-01
        df.set_index('时间点', inplace=True)
        df = df.resample('30T').first()
        print(f"时间抽样后第一条：\n{df}")
        # print(f"on档：\n{df[df['电源档位_(12D)']==3.0]}")  # 注意这样的输出是没有时间断层的数据的。不包含空值
        df = df[~((df['电源档位_(12D)'] == 3.0) | (df['充电枪连接状态_(344)'].isin([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])))]
        print(f"on档补集：\n{df}")  # 补集后面要加括号

    # 读取文件名字
    import os
    filename = os.path.basename(save_path)
    print(f"文件名字：{filename.split('.')[0]}")
    df['vin'] = filename.split('.')[0]   #如果df是空，那么df['vin']也是空，
    print(f"on档补集添加vin：\n{df['vin']}")  # 补集后面要加括号


if __name__ == '__main__':
    print('a')
    # 下载~分析
    # def_job = {'login': True, 'submit': True, 'down': True, 'decode': True, 'concat': False, 'tell_me': '准备下载数据', 'analyse': True}  # 默认工作流开关控制
    # 登录、解码、分析
    def_job = {'login': True, 'submit': False, 'down': False, 'decode': True, 'concat': False, 'tell_me': '数据下载完成', 'analyse': True}  # 默认工作流开关控制
    # 只分析
    # def_job = {'login': False, 'submit': False, 'down': False, 'decode': False, 'concat': False, 'tell_me': '准备下载数据', 'analyse': True}  # 默认工作流开关控制

    if def_job['login']:
        (token, b, c) = login()
    # path1 = r'D:\大数据工作\01数据分析\01临时分析\丑新龙OK上电次数\20240123\上电次数查询明细.xlsx'
    # path1 = r'./01后台大数据/发动机水泵故障明细-宋PLUS.xlsx'  # 业务文件
    # df = pd.read_excel(path1,parse_dates=['生产日期','购车日期'])
    now = datetime.datetime.now()
    # input_path = f".\数据存储/秦PD4.00.02OTA升级结果明细.xlsx"
    input_path = fr"./数据存储/{str(now.date())}/第一次推送（处理）.xlsx"
    # path1 = r'./01后台大数据/发动机水泵故障明细-宋PLUS.xlsx'  # 业务文件
    # df = pd.read_excel(path1,parse_dates=['生产日期','购车日期'])
    # df = pd.read_excel(input_path, sheet_name='第二批明细')['VIN'][1:2]
    vin_cnt = int(input(f"下载几台车？"))
    print(f"下载 {vin_cnt} 台车")
    df = pd.read_excel(input_path)['VIN'][:vin_cnt]  #[:]
    # AttributeError: 'Series' object has no attribute 'columns'
    vins = df.drop_duplicates().to_list()
    vins = [i.replace(' ', '') for i in vins]  # 去掉vin中的空字符串
    # vins = ['LGXEK1C42P0902909']   # 测试一辆车，探查数据下载情况
    print(f'共 {len(vins)} 辆车: {vins}')

    # freq_type = '8'  # 0=30s， 1=1s, 8=高精度
    freq_type = '0'  # 0=30s， 1=1s, 8=高精度
    data_type = 'High_Precision(R)'  # 4.0, 高精度 , High_Precision(R)
    df_signal = pd.read_excel(r'..\00-bd-monitor\file\signal-total.xlsx', sheet_name='总表')
    # searsh_title = ['.*FMCU.*IGBT温度.*464', '.*RMCU.*IGBT温度.*464']  # 只能设计成第几个信号关键词，同一个信号的多个关键词用英文逗号分隔，不同信号之间用英文分号分隔
    # searsh_title = ['.*车辆当前故障.*387.*', '.*车辆当前故障.*324.*']  # 不能包含括号，如果包含必须进行转义。只能设计成第几个信号关键词，同一个信号的多个关键词用英文逗号分隔，不同信号之间用英文分号分隔
    searsh_title = ['.*电源档位.*12D.*', '.*充电枪连接状态.*344.*']  # 不能包含括号，如果包含必须进行转义。只能设计成第几个信号关键词，同一个信号的多个关键词用英文逗号分隔，不同信号之间用英文分号分隔
    # print(df_signal['id'].dtypes)  # 数据类型是int64
    df_signal = df_signal[(df_signal['data_type']==data_type)  # 4.0, 高精度
                   & df_signal['title'].str.contains('|'.join(str(st) for st in searsh_title), regex=True)]
    print(f"共 {len(df_signal)} 个信号，{df_signal['id'].tolist()}，{df_signal[['id', 'title']]}")

    signal_list = df_signal['id'].tolist()  # 电源档位_(12D)
    # signal_list = [i.replace(' ', '') for i in signal_list]  # 去掉 signal_list 中的空字符串
    # AttributeError: 'int' object has no attribute 'replace'
    # print(signal_list, type(signal_list))
    input = input(f"请确认信号信息！1==,0")
    s_time = '2024-03-05 00:00:00'
    e_time = '2024-03-05 23:59:59'

    now = datetime.datetime.now()
    start_time = now - datetime.timedelta(days=0, seconds=5)  # 今天
    step = 1000  # 一次性提交多少辆车，当车辆数大于500的时候, 最多提交10次，大于10次后台没有显示
    if def_job['submit']:
        for i in range(0, len(vins), step):  # start，stop，step
            if i + step > len(vins):
                vins_list = vins[i:len(vins)]
            else:
                vins_list = vins[i: i + step]
            submit_cnt = int(i/step) + 1
            # if submit_cnt < 1:  # 避免任务被中途取消后，接着之前下载的数据继续做。 从第几次开始就填几
            #     continue

            print(f"第{submit_cnt}次提交：车辆数：{len(vins_list)} ")

            submit_list = [vins_list, signal_list, s_time, e_time, data_type, freq_type, token]
            # submit_list = [vins_list, signal_list, s_time, e_time, 'High_Precision(R)', '8', token]  #仰望
            submit_data(submit_list)
            time.sleep(10)

    # t = 0  # 初始下载次数
    # tell_me = '准备下载数据'
    # 文件夹名称
    save_path = f"./数据存储/{str(now.date())}/{data_type}_{freq_type}"
    os.path.exists(save_path) or os.makedirs(save_path)

    if def_job['down']:    # 提交次数≠下载次数就去一直下载
        def_job['tell_me'] = download(token=token, start_time=start_time, save_path=save_path)

    if def_job['tell_me'] == '数据下载完成':
        dic_vin = vin_transform(vins, token)
        decode_path = f"./数据存储/{str(now.date())}/decode"
        os.path.exists(decode_path) or os.makedirs(decode_path)
        code2vin(dic_vin=dic_vin, file_path=save_path, decode_path=decode_path)
        time.sleep(5)
    # if def_job['concat'] and def_job['tell_me'] == '数据下载完成':
    if def_job['concat']:
        concat_all_data()
    if df_total is not None or def_job['analyse']:
        # demo_single(df_total)  #单个文件分析
        demo_more(df_total)   # 逐个分析单个文件并合并结果集
        # anslyse_0226(df_total)  # 合并后的分析





    # t=1
    # for i in df_s['上OK次数'].value_counts().index:
    #     df = df_s[df_s['上OK次数'].astype('str') == str(i)]
    #
    #     if len(i)==1:
    #         s_time = f'2023-0{i[0]}-01 00:00:00'
    #         e_time = str(datetime.datetime.strptime(f'2023-0{i[0]}-01 00:00:00','%Y-%m-%d %H:%M:%S')+ relativedelta(months=1))
    #     else:
    #         s_time = f'2023-0{i[0]}-01 00:00:00'
    #         e_time = str(datetime.datetime.strptime(f'2023-0{i[-1]}-01 00:00:00','%Y-%m-%d %H:%M:%S')+ relativedelta(months=1))
    #
    #     vins = df['VIN号'].to_list()
    #     submit_list = [vins, signal_list, s_time, e_time, '4.0', '0', token]
    #     submit_data(submit_list)
    #     time.sleep(2)
    #     now = datetime.datetime.now()
    #     start_time = now - datetime.timedelta(minutes=1)
    #     path_save = f"./data/{str(t)}"
    #     tell_me = download(token=token, start_time=start_time,save_path=path_save)
    #     if tell_me == '数据下载完成':
    #         # vin转换
    #         dic_vin = vin_transform(vins, token)
    #         code2vin(dic_vin=dic_vin, file_path=path_save)
    #         t+=1
    #
    # t=0
    # for i in range(0,df_s['VIN号'].count(),500):
    #     t+=1
    #     df1=df_s.truncate(before=i,after=i+499)
    #     print(df1)
    #     vins = df1['VIN号'].to_list()
    #
    #     submit_list = [vins, signal_list, s_time, e_time, '4.0', '0', token]
    #
    #     '''
    #     传入一个submit_list
    #     0、VIN（列表形式）
    #     1、信号id（列表形式）
    #     2、数据起始时间（20xx-x-x xx:xx:xx）
    #     3、数据结束时间
    #     4、协议平台："4.0" 、"High_Precision(4.0)" = 高精度、"High_Precision(R)" = R协议
    #     5、dataSource：数据源选择 ：'0'=30s，'1'=1s，'8'=高精度
    #     6、token
    #     submit_list=[VIN列表，信号id列表，起始时间，结束时间，协议平台，数据源选择，token]
    #     '''
    #
    #     submit_data(submit_list)
    #     time.sleep(2)
    #     now = datetime.datetime.now()
    #     start_time = now - datetime.timedelta(minutes=1)
    #     path_save = f"./data/{str(t)}"
    #     tell_me = download(token=token, start_time=start_time,save_path=path_save)
    #     if tell_me == '数据下载完成':
    #         # vin转换
    #         dic_vin = vin_transform(vins, token)
    #         code2vin(dic_vin=dic_vin, file_path=path_save)