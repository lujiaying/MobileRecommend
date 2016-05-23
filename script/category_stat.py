# coding: utf-8
'''商品品类级别的统计'''

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
    category_dict = {}
    with open(train_item_path) as fopen:
        fopen.readline()
        for line in fopen:
            line_list = line.strip().split(',')
            user_id,item_id,behavior_type,user_geohash,item_category,time = line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]
            if item_category not in category_dict:
                category_dict[item_category] = {'category_id': item_category,'item_ids': set(), 'view_pv':0, 'collect_pv':0, 'cart_pv':0, 'buy_pv':0, 'view_uids':set(), 'collect_uids':set(), 'cart_uids':set(), 'buy_uids':set()}
            behavior_type_str = behavior_map[int(behavior_type)]
            category_dict[item_category][behavior_type_str+'_pv'] += 1
            category_dict[item_category]['item_ids'].add(item_id)
            category_dict[item_category][behavior_type_str+'_uids'].add(user_id)

    # step 2, calculate
    logger.info('Start calculate uv')
    for category_id, info_dict in category_dict.iteritems():
        info_dict['view_uv'] = len(info_dict['view_uids'])
        info_dict['collect_uv'] = len(info_dict['collect_uids'])
        info_dict['cart_uv'] = len(info_dict['cart_uids'])
        info_dict['buy_uv'] = len(info_dict['buy_uids'])
        info_dict['item_num'] = len(info_dict['item_ids'])

    # step 3, output
    logger.info('Start output')
    output_path = '%s/feature/category_basic_stat.csv' % (abs_father_path)
    with open(output_path, 'w') as fopen:
        col_names = ['category_id', 'item_num', 'view_pv', 'collect_pv', 'cart_pv', 'buy_pv', 'view_uv', 'collect_uv', 'cart_uv', 'buy_uv']
        fopen.write(','.join(col_names) + '\n')
        for category_id, info_dict in category_dict.iteritems():
            col_num_list = [str(info_dict[col]) for col in col_names]
            fopen.write(','.join(col_num_list) + '\n')

if __name__ == '__main__':
    main()
