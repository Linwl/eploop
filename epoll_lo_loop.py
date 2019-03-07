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
        self.connections={}
        self.requests={}
        self.responses={}


    def start(self):
        while 1:
            events = self.epoll.epoll()
            for fileno,event in events:
                if fileno == self.server.fileno():
                    print('有客户连接进入')
                    connection, addr = self.server.accept()
                    connFd = connection.fileno()#获取连接句柄
                    connection.setblocking(False)
                    self.epoll.register(connFd, select.EPOLLIN)#注册epoll的读事件
                    self.connections[connFd] = connection
                elif event & select.EPOLLHUP:
                    print('客户连接已断开')
                    # 销毁已断开的客户端socket句柄
                    self.epoll.unregister(fileno)
                    # 关闭客户端socket连接
                    self.connections[fileno].close()
                    #剔除该客户端
                    self.connections.pop(fileno)
                elif event & select.EPOLLIN:
                    # 接收数据
                    self.requests[fileno] = self.connections[fileno].recv(1024).strip()
                    # 将客户端文件句柄整形的从EPOLLIN中转移到 EPOLLOUT
                    self.epoll.modify(fileno, select.EPOLLOUT)
                elif event & select.EPOLLOUT:
                    # 发送数据
                    self.connections[fileno].send(self.requests[fileno])
                    # 将客户端文件句柄整形的 从EPOLLOUT中转移到 EPOLLHUP
                    self.epoll.modify(fileno, select.EPOLLHUP)
