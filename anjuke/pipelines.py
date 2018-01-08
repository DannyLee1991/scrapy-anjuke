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

    def process_item(self, item, spider):
        log.msg("插入数据库", log.DEBUG)
        sql = self.sql_insert_or_ignore(item)
        self.conn.execute(sql)
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        sql = self.sql_create()
        conn.execute(sql)
        conn.commit()
        return conn

    def sql_create(self):
        sql = """CREATE TABLE %s
                     (
                     ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     TITLE VARCHAR,
                     GUARANTEE_INFO VARCHAR,
                     LINK VARCHAR NOT NULL UNIQUE,
                     AREA VARCHAR,
                     HOUSE_TYPE VARCHAR,
                     FLOOR_INFO VARCHAR,
                     BUILD_TIME_INFO INTEGER,
                     BROKER_NAME VARCHAR,
                     ADDRESS VARCHAR,
                     LOCATE_A VARCHAR,
                     LOCATE_B VARCHAR,
                     TAGS VARCHAR,
                     PRICE INTEGER,
                     UNIT_PRICE INTEGER,
                     GET_TIME VARCHAR
                     )""" % (self.table)
        return sql

    def sql_insert_or_ignore(self, item):
        sql = """INSERT OR IGNORE INTO {table_name} 
            (TITLE,
            GUARANTEE_INFO,
            LINK,
            AREA,
            HOUSE_TYPE,
            FLOOR_INFO,
            BUILD_TIME_INFO,
            BROKER_NAME,
            ADDRESS,
            LOCATE_A,
            LOCATE_B,
            TAGS,
            PRICE,
            UNIT_PRICE,
            GET_TIME
            ) VALUES (
            "{title}",
            "{guarantee_info}",
            "{link}",
            "{area}",
            "{house_type}",
            "{floor_info}",
            "{build_time_info}",
            "{broker_name}",
            "{address}",
            "{locate_a}",
            "{locate_b}",
            "{tags}",
            {price},
            {unit_price},
            "{get_time}")
            """.format(
            table_name=self.table,
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
