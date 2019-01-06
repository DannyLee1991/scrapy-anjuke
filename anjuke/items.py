# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    house_id = scrapy.Field() # 房屋id
    title = scrapy.Field()  # 楼盘名称
    guarantee_info = scrapy.Field()  # 安选验真信息
    link = scrapy.Field()  # 链接
    area = scrapy.Field()  # 面积
    house_type = scrapy.Field()  # 户型
    floor_info = scrapy.Field()  # 楼层信息
    build_time_info = scrapy.Field()  # 建造时间信息
    broker_name = scrapy.Field()  # 经纪人姓名
    address = scrapy.Field()  # 地址
    locate_a = scrapy.Field()  # 一级区域信息 eg：浦东
    locate_b = scrapy.Field()  # 二级区域信息 eg：张江
    tags = scrapy.Field()  # 地址
    price = scrapy.Field()  # 价格
    unit_price = scrapy.Field()  # 每平米价格
    get_time = scrapy.Field() # 数据获取时间

