# -*-coding:utf-8 -*-
"""
在ios上实现短信上行自动接收并写入数据库
author @boole
date 2019-05-12
"""
import os
import time
import json
import datetime
from biplist import *

# 获取当前时间
now_t = datetime.datetime.now()
timeStamp = int(time.mktime(now_t.timetuple()))


def file_create_time(f_Path):
    """
    获取文件创建时间
    :param f_Path:
    :return:
    """
    t = os.path.getctime(f_Path)
    return int(t)


def decode_meg(f_path):
    """
    解析Plist文件
    :param f_path:
    :return:
    """
    msg_list = []
    plist = readPlist(f_path)
    for info in plist["$objects"]:
        if type(info) == dict:
            if "NS.string" in info:
                msg_list.append(info["NS.string"])
    return msg_list


def ergodic(m_path, out_f, time_diff):
    """
    遍历根目录并将解析数据写入指定文件
    :param m_path:
    :param out_f:
    :param time_diff:
    :return:
    """
    file_list = os.listdir(m_path)
    out_msg = {}
    for i in range(len(file_list)):
        file_path = m_path + file_list[i]
        ct = file_create_time(file_path)
        # 解析指定时间内的文件(这里加了5s，是为了给程序计算留出时间，一般没必要)
        if (timeStamp - ct) < time_diff + 5:
            msg = decode_meg(file_path)
            out_msg[i] = {"u": msg[-1], "v": msg[-2], "t": ct}
        # 写入数据库，这里作为demo，写入本地文件
        with open(out_f, "w") as f:
            json.dump(out_msg, f)


def polling(r_path):
    """
    定期轮询文件
    :param r_path:
    :return:
    """
    i = 1
    while True:
        dt = datetime.date.today().strftime('%Y-%m-%d')
        # dt = "2019-05-12"
        msg_path = r_path + dt + '/'
        out_file = "./dat/uplink_msg.json"
        time_diff = 60  # 每60s轮询一次
        ergodic(msg_path, out_file, time_diff)
        print("这是第 %s 次轮询" % i)
        time.sleep(time_diff)
        i += 1
        if i > 10:
            break

if __name__ == '__main__':
    # 获取文件地址
    root_path = "/Users/xxx/Library/Messages/Archive/"
    polling(root_path)
