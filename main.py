#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Linwl
# @Date  : 2019/3/7
# @Desc  :
from epoll_lo_loop import EpollIOLoop

if __name__ == '__main__':
    try:
        loop = EpollIOLoop()
        loop.start()
    except Exception as e:
        print(e)