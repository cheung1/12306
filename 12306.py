# !/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'Cheung'

import requests
from info import *          #import '*' 则不需要 .调用 ，直接写参数名
import cons                 # 只 import ，需要 cons. 来调用
import damatuWeb

req = requests.Session()

dict_station = {}
temp_li = cons.station.split('@')
for i in temp_li:
    temp_list = i.split('|')
    if len(temp_list) > 3:  # 确保 temp_list 中，一定有 名称(index = 1)和对应编码(index = 2)
        dict_station[temp_list[1]] = temp_list[2]  # 将 temp_list[1] 做为 key, temp_list[2] 做为 value
# print(dict_station)

from_station = dict_station[FROM_STATION]
to_station = dict_station[TO_STATION]

# print(from_station,to_station)

def query_tickets():
    response = req.get(
        '{}?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(TRAIN_URL, TRAIN_DATE, from_station, to_station)
    )
    result = response.json()
    return result['data']['result']

def login():
    print('正在加载验证码图片...')
    response = req.get('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.05653796953739176')
    imageCode = response.content
    fn = open('code.png','wb')
    fn.write(imageCode)
    fn.close()
    data = {
        'answer' : damatuWeb.getCode(),        # 验证码坐标
        'login_site' : 'E',
        'rand' : 'sjrand'
    }
    response = req.post('https://kyfw.12306.cn/passport/captcha/captcha-check', data=data, headers=cons.headers)
    result = response.json()
    if result['result_code'] != '4':
        login()
        return
    data = {
        'username' : user,
        'password' : pwd,
        'appid' :'otn'
    }
    response = req.post('https://kyfw.12306.cn/passport/web/login', data=data, headers=cons.headers)
    print(response.text)

login()

'''
    硬座 = 29
    硬卧 = 28
    无座 = 26
    软座 = 25
    软卧 = 23
    一等座 = 31
    二等座 = 30
    车次 = 3
    商务座特等座 = 32
'''

# for i in query_tickets():
#     temp_list = i.split('|')
#     # temp_index = list(enumerate(temp_list))
#     # print(temp_index)
#
#     # hard_bed = temp_list[HARD_BED]
#     # no_seat = temp_list[NO_SEAT]
#     # soft_bed = temp_list[SOFT_BED]
#     # first_seat = temp_list[FIRST_SEAT]
#     # second_seat = temp_list[SECOND_SEAT]
#     # head_seat = temp_list[HEAD_SEAT]
#
#     hard_seat = temp_list[HARD_SEAT]
#     seat = temp_list[HARD_SEAT]
#     # print(type(seat))
#     if seat == '' or seat == '无':
#         print('无票', seat, temp_list[3])
#     else:
#         print('有票', seat, temp_list[3])







