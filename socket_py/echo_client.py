# -*- coding: utf-8 -*-
"""
压力测试
"""
import os
import socket
import configparser

conf_dir = os.path.abspath(os.path.join(os.getcwd(), "./conf/server.conf"))
cp = configparser.ConfigParser()
cp.read(conf_dir)
IP = cp.get('host', "ip")
PORT = int(cp.get('host', "port"))

text = '19\na b c d e f g h\n'


def client():
    """
    单例请求
    :return:
    """
    addr = (IP, PORT)
    s = socket.socket()
    s.connect(addr)
    for i in range(5):
        s.send(bytes(text, encoding="utf-8"))
        data = s.recv(1024)
        print(data)


def mulClient():
    """
    并发请求
    :return:
    """
    socks = []
    addr = (IP, PORT)
    for i in range(100):
        socks.append(socket.socket())

    for s in socks:
        s.connect(addr)

    for i in range(1000):
        for s in socks:
            s.send(bytes(text, encoding="utf-8"))
            data = s.recv(1024)
            # print(data)


if __name__ == '__main__':
    client()


