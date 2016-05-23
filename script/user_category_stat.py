# coding: utf-8
'''对用户X品牌的统计'''

__author__ = 'lujiaying'

import os
import sys
abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
sys.path.append(abs_father_path)
from utils.log_tools import feature_logger as logger

behavior_map = {1:'view', 2:'collect', 3:'cart', 4:'buy'}

def main():
    '''
    main work flow
    '''
    # step 1, read raw data
    train_item_path = '%s/data_source/tianchi_mobile_recommend_train_user.csv' % (abs_father_path)
    logger.info('Start read from %s' % (train_item_path))
    user_dict = {}
    with open(train_item_path) as fopen:
        fopen.readline()
        for line in fopen:
            line_list = line.strip().split(',')
            user_id,item_id,behavior_type,user_geohash,item_category,time = line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]
            behavior_type_str = behavior_map[int(behavior_type)]
            if user_id not in user_dict:
                user_dict[user_id] = {'user_id':user_id, 'view':0, 'collect':0, 'cart':0, 'buy':0, 'view_item_set':set(), 'collect_item_set':set(), 'cart_item_set':set(), 'buy_item_set':set(), 'view_category_set':set(), 'collect_category_set':set(), 'cart_category_set':set(), 'buy_category_set':set()}
            user_dict[user_id][behavior_type_str] += 1
            user_dict[user_id][behavior_type_str+'_item_set'].add(item_id)
            user_dict[user_id][behavior_type_str+'_category_set'].add(item_category)


    # step 2, calculate
    logger.info('Start calculate uv')
    for user_id, info_dict in user_dict.iteritems():
        info_dict['view_item_num'] = len(info_dict['view_item_set'])
        info_dict['collect_item_num'] = len(info_dict['collect_item_set'])
        info_dict['cart_item_num'] = len(info_dict['cart_item_set'])
        info_dict['buy_item_num'] = len(info_dict['buy_item_set'])
        info_dict['view_category_num'] = len(info_dict['view_category_set'])
        info_dict['collect_category_num'] = len(info_dict['collect_category_set'])
        info_dict['cart_category_num'] = len(info_dict['cart_category_set'])
        info_dict['buy_category_num'] = len(info_dict['buy_category_set'])

    # step 3, output
    logger.info('Start output')
    output_path = '%s/feature/user_basic_stat.csv' % (abs_father_path)
    with open(output_path, 'w') as fopen:
        col_names = ['user_id', 'view', 'collect', 'cart', 'buy', 'view_item_num', 'collect_item_num', 'cart_item_num', 'buy_item_num', 'view_category_num', 'collect_category_num', 'cart_category_num', 'buy_category_num']
        fopen.write(','.join(col_names) + '\n')
        for category_id, info_dict in user_dict.iteritems():
            col_num_list = [str(info_dict[col]) for col in col_names]
            fopen.write(','.join(col_num_list) + '\n')

if __name__ == '__main__':
    main()
