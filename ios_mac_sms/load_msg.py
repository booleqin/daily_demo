# -*-coding:utf-8 -*-
"""
加载信息，实际环境中这里应该是数据库方法
author @boole
date 2019-05-09
"""

import json

out_file = "./dat/uplink_msg.json"
with open(out_file, 'r') as load_f:
    load_dict = json.load(load_f)

for k, v in load_dict.items():
    print(v)

