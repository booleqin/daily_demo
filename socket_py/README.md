# python实现简单Server

## 实现内容
接收一个字符串，过滤掉该字符串中全部空格返回给客户端

eg：
    REQUEST = '15\na b c d e f\n'
    RESPONSE = '10\nabcdef\n'

## 运行

    1. 指定HOST ——> 在conf中指定ip和port
    2. 启动server服务 ——> sh server_run.sh start （参数包括 start|stop|restart|status）
    3. 启动客户端 ——> python echo_client.py （包含单例请求和并发请求）

## 日志记录
请求ip，请求包长度，响应包长度，是否成功，请求耗时

eg:

    2019/06/04 19:29:31 | INFO | 74 | echo_server | 127.0.0.1 | 15 | 10 | OK | 8.225440979003906e-05
    2019/06/04 19:29:31 | INFO | 74 | echo_server | 127.0.0.1 | 15 | 10 | OK | 2.193450927734375e-05
    2019/06/04 19:29:31 | INFO | 74 | echo_server | 127.0.0.1 | 15 | 10 | OK | 1.2159347534179688e-05
    2019/06/04 19:29:31 | INFO | 74 | echo_server | 127.0.0.1 | 15 | 10 | OK | 1.4066696166992188e-05
    2019/06/04 19:29:31 | INFO | 74 | echo_server | 127.0.0.1 | 15 | 10 | OK | 1.3113021850585938e-05

## 压力测试

使用客户端并发请求近似压测

100个socket完成总计10万次请求，耗时近8s，每秒响应量(qps)约为13000

## 附（socket数据流）

<img src="./dat/socket_flow.png" width = "300" height = "500" alt="socket数据流" align=center />

