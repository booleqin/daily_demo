# -*- coding: utf-8 -*-
"""
服务端
created by qinyangyang @ 2019-06-01
"""
import os
import socket
import selectors
import time
import logging
import configparser

conf_dir = os.path.abspath(os.path.join(os.getcwd(), "./conf/server.conf"))
cp = configparser.ConfigParser()
cp.read(conf_dir)
IP = cp.get('host', "ip")
PORT = int(cp.get('host', "port"))

# 日志配置
logging.basicConfig(level=logging.DEBUG,
                    filename='./log/server.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s | %(levelname)s | %(lineno)d | %(module)s | %(message)s')
logger = logging.getLogger(__name__)


sel = selectors.DefaultSelector()


def accept(sock, mask):
    """
    监听客户端发送进来的数据
    :param sock:
    :param mask:
    :return:
    """
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    """
    监听有数据可读事件
    :param conn:
    :param mask:
    :return:
    """
    sTime0 = time.time()
    host = input_len = output_len = None
    try:
        data = conn.recv(1024)
        host = conn.getpeername()
        # host = ':'.join([str(x) for x in host])
        host = host[0]
    except ConnectionResetError as e:
        timeConsum = str(time.time() - sTime0)
        log_info = [host, input_len, output_len, 'client send data to server error', timeConsum]
        logger.error(' | '.join(log_info))
        # print('客户端在发送数据到服务端时异常退出，服务端关闭该连接', conn)
        sel.unregister(conn)
        conn.close()

    if data:
        sTime = time.time()
        data = data.decode('utf-8')
        dataList = data.strip().split('\n')
        str_text = dataList[1].replace(" ", "")
        str_len = len(str_text) + 2 * len('\n')
        len_len = len(str(str_len))
        out_len = str_len + len_len
        out = [str(out_len), "\n", str_text, "\n"]
        # dataList = data.split(b' ')
        text = ''.join(out)
        try:
            conn.send(bytes(text, encoding="utf-8"))
            input_len = str(len(data))
            output_len = str(len(text))
            timeConsum = str(time.time() - sTime)
            log_info = [host, input_len, output_len, 'OK', timeConsum]
            logger.info(' | '.join(log_info))
        except ConnectionResetError as e:
            timeConsum = str(time.time() - sTime)
            log_info = [host, input_len, output_len, 'server send data to client error', timeConsum]
            logger.error(' | '.join(log_info))
            # print('服务端向客户端发送数据时异常退出，服务端关闭该连接', conn)
            sel.unregister(conn)
            conn.close()
    else:
        # timeConsum = str(time.time() - sTime0)
        # log_info = [host, input_len, output_len, 'server sign out', timeConsum]
        # logger.info(' | '.join(log_info))
        # print('客户端正常退出，服务端关闭连接', conn)
        sel.unregister(conn)
        conn.close()


def server():
    """
    服务端server
    :return:
    """
    sock = socket.socket()
    sock.bind((IP, PORT))
    sock.listen()
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    server()

