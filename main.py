# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 13:03
# @Author  : AsiHacker
# @File    : main
# @Software: PyCharm
# @notice  : True masters always have the heart of an apprentice.
import os
import time

import psutil
from flask import Flask, jsonify

from help import check_proxy_ok

app = Flask(__name__)

DOMESTIC_ADDRESS = '119.23.111.99'
FOREIGN_ADDRESS = '47.241.243.39'


@app.route('/socks5_to_ssr/<string:origin_proxy>/<int:to_port>', methods=['GET'])
def socks5_to_ssr(origin_proxy: str, to_port: int):
    """
    # 10000-20000
    92.119.161.43:50149:JTKRTQCG:kqPjwccD
    :param origin_proxy:
    :param to_port:
    :return:
    """
    if to_port not in range(10000, 20000):
        return jsonify(code=200, msg='to_port in 10000-20000')
    pid = check_proxy_ok(to_port)
    if pid is not None:
        psutil.Process(int(pid)).kill()
    origin_proxy_list = origin_proxy.split(':')
    if len(origin_proxy_list) != 4:
        return jsonify(code=201, msg='Incorrect format')
    cmd = f'pproxy -r socks5://{origin_proxy_list[0]}:{origin_proxy_list[1]}#{origin_proxy_list[2]}:{origin_proxy_list[3]} -l ssr://chacha20:nantian888@0.0.0.0:{to_port} --daemon'
    os.system(cmd)
    time.sleep(3)
    pid = check_proxy_ok(to_port)
    if pid is not None:
        return jsonify(code=200, msg='ok',
                       data={'url': f'ssr://chacha20:nantian888:{FOREIGN_ADDRESS}:{to_port}', 'pid': pid})
    else:
        return jsonify(code=201, msg='Failed to open')


@app.route('/ssr_to_socks5/<string:origin_proxy>/<int:to_port>', methods=['GET'])
def ssr_to_socks5(origin_proxy: str, to_port: int):
    """
    # 10000-20000
    chacha20:nantian888@47.241.208.24:2000
    :param origin_proxy:
    :param to_port:
    :return:
    """
    if to_port not in range(10000, 20000):
        return jsonify(code=200, msg='to_port in 10000-20000')
    pid = check_proxy_ok(to_port)
    if pid is not None:
        psutil.Process(int(pid)).kill()
    origin_proxy_list = origin_proxy.split(':')
    if len(origin_proxy_list) != 4:
        return jsonify(code=201, msg='Incorrect format')
    cmd = f'pproxy -r ssr://{origin_proxy_list[0]}:{origin_proxy_list[1]}@{origin_proxy_list[2]}:{origin_proxy_list[3]} -l socks5://0.0.0.0:{to_port} --daemon'
    os.system(cmd)
    time.sleep(3)
    pid = check_proxy_ok(to_port)
    if pid is not None:
        return jsonify(code=200, msg='ok',
                       data={'url': f'socks5://{DOMESTIC_ADDRESS}:{to_port}', 'pid': pid})
    else:
        return jsonify(code=201, msg='Failed to open')


if __name__ == '__main__':
    app.run(port=39001, debug=True, host='0.0.0.0')
