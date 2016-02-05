# -*- coding:utf-8 -*-
import ConfigParser

__author__ = 'licong'

class Config(object):
    def __init__(self, config_file_name):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file_name)
        
        self.page_nums = self.cf.get('common','page_nums')
        self.db_file = self.cf.get('db','db_file_name')
        self.result_file = self.cf.get('db', 'result_file_name')
        
