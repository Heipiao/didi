#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 07:01:47
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 

import os


## import python`s own lib

## import third party lib

## import local lib


def deal_the_day(x):
    if(x.day<10):
        return str(x.year)+'-'+'0'+str(x.month)+'-'+'0'+str(x.day)+'-'+str(x.hour*6+int(x.minute/10)+1)
    else:
        return str(x.year)+'-'+'0'+str(x.month)+'-'+str(x.day)+'-'+str(x.hour*6+int(x.minute/10)+1)