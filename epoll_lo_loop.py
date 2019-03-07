#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : epoll_lo_loop.py
# @Author: Linwl
# @Date  : 2019/3/7
# @Desc  : epoll主循环

import select
import socket

class EpollIOLoop:

    def __init__(self):
        self.server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 设置socket为ip address复用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 9090))
        self.server.listen(1000)
        self.server.setblocking(False)#设置为非阻塞
        self.epoll = select.epoll()
        self.epoll.register(self.server.fileno(),select.EPOLLIN)

    def start(self):
        while 1:
            pass