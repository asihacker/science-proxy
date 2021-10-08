# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 13:11
# @Author  : AsiHacker
# @File    : help
# @Software: PyCharm
# @notice  : True masters always have the heart of an apprentice.
import socket

import psutil as psutil


def check_port_in_use(port, host='0.0.0.0'):
    """
    检测端口是否被占用
    :param port:
    :param host:
    :return:
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()


def check_proxy_ok(to_port: int):
    """
    检测代理是否成功
    :param to_port:
    :return:
    """
    for proc in psutil.process_iter():
        try:
            info = proc.as_dict(attrs=['pid', 'name', 'connections', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if info['connections'] and \
                    'proxy' in '|'.join(info['cmdline']) and to_port == info['connections'][0].laddr.port:
                return info['pid']
    return None
