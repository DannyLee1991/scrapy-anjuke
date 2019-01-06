# -*- coding: utf-8 -*-
from tools import remove_query_args, now_timestamp
from scrapy.exceptions import DropItem
import sqlite3
from os import path
from scrapy import log

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from anjuke.settings import DB_NAME


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AnjukePipeline(object):
    def process_item(self, item, spider):
        # 数据预处理
        log.msg("数据预处理", log.DEBUG)
        self.process_locate_info(item)
        self.process_link_info(item)
        self.process_unit_price(item)
        self.porcess_area_info(item)
        self.process_buildtime_info(item)
        item['get_time'] = now_timestamp()
        return item

    def process_locate_info(self, item):
        '''
        处理地址数据
        根据地址信息，获取区域信息
        eg: 浦东  张江
        :return:
        '''
        sub_address = item["address"].strip().split('\n')[1].strip()
        strs = sub_address.split('-')
        locate_a = strs[0]
        locate_b = strs[1]
        item['locate_a'] = locate_a
        item['locate_b'] = locate_b

    def process_link_info(self, item):
        '''
        处理链接数据  移除后面的请求参数
        :param item:
        :return:
        '''
        link = item['link']
        item['link'] = remove_query_args(link)

    def process_unit_price(self, item):
        # 之前 unit_price 是 这种形式 53571元/m²,
        # 处理后 是 这种形象 53571
        item['unit_price'] = item['unit_price'][:-4]

    def porcess_area_info(self, item):
        # 25m² -> 25
        item['area'] = item['area'][:-2]

    def process_buildtime_info(self, item):
        # 2015年建造  ->  2015
        item['build_time_info'] = item['build_time_info'][:-3]


class Unvalue_remover_Pipeline(object):
    """
    数据过滤
    """

    def process_item(self, item, spider):
        if item['link']:
            return item
        else:
            raise DropItem("无效数据移除: {0}".format(item))


class SQLiteStorePipeline(object):
    '''
    将数据存储在sqlite中
    '''
    filename = DB_NAME
    table = "anjuke_data"

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = sqlite3.connect(self.filename)
            sql = self.sql_create()
            self.execute_sql(sql, commit=True)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def process_item(self, item, spider):
        log.msg("插入数据库", log.DEBUG)
        sql = self.sql_insert_or_ignore(item)
        self.execute_sql(sql)
        return item

    def execute_sql(self, sql, commit=True):
        '''
        执行sql
        :param sql:
        :return:
        '''
        log.msg("执行sql > {sql}".format(sql=sql))
        self.conn.execute(sql)
        if commit:
            self.conn.commit()

    def load_sql_file(self, file_name):
        '''
        根据文件名加载文件中的sql语句
        :param file_name:
        :return:
        '''
        with open('./sql/' + file_name, 'r') as f:
            sql = f.read()
            return sql

    def sql_create(self):
        '''
        建表语句
        :return:
        '''
        sql = self.load_sql_file("create_anjuke_data.sql").format(table_name=self.table)
        return sql

    def sql_insert_or_ignore(self, item):
        '''
        插入数据语句
        :param item:
        :return:
        '''
        sql = self.load_sql_file("insert_anjuke_data.sql").format(
            table_name=self.table,
            house_id=item['house_id'],
            title=item['title'],
            guarantee_info=item['guarantee_info'],
            link=item['link'],
            area=item['area'],
            house_type=item['house_type'],
            floor_info=item['floor_info'],
            build_time_info=item['build_time_info'],
            broker_name=item['broker_name'],
            address=item['address'],
            locate_a=item['locate_a'],
            locate_b=item['locate_b'],
            tags=item['tags'],
            price=item['price'],
            unit_price=item['unit_price'],
            get_time=item['get_time']
        )
        return sql
