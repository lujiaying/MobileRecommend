# -*- coding: utf-8 -*-
'''
数据处理工具
Author: lujiaying
Date: 2016/06/06
'''

import datetime

def str2datetime(time_str):
    '''
    Args:
        time_str: string

    Returns:
        time_dtime: datetime.datetime
    '''
    time_dtime = datetime.datetime.strptime(time_str, '%Y-%m-%d %H')
    return time_dtime
