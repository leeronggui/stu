#coding:utf-8
import app
import db


def diff_keys(improve, all_key):
    '''
    :param improve:list
    :param all_key:list
    :return:
    '''
    diff_list = []
    improve_set = set(improve)
    all_key_set = set(all_key)
    if improve_set | all_key_set != all_key_set:diff_list = list(all_key_set ^ improve_set)
    return diff_list

