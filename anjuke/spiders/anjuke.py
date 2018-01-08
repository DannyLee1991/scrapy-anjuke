import scrapy

from anjuke.items import AnjukeItem


class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]

    def start_requests(self):
        urls = [
            'https://shanghai.anjuke.com/sale/p1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = AnjukeItem()
        print('------------------------------------------------')
        info_list = response.xpath("//*[@id='houselist-mod-new']/li")
        for info in info_list:
            # 标题
            title = info.xpath("./div[2]/div[1]/a/text()").extract()
            # 安选验真信息
            guarantee_info = info.xpath("./div[2]/div[1]/em/@title").extract()
            # 链接
            link = info.xpath("./div[2]/div[1]/a/@href").extract()
            # 户型
            house_type = info.xpath("./div[2]/div[2]/span[1]/text()").extract()
            # 面积
            area = info.xpath("./div[2]/div[2]/span[2]/text()").extract()
            # 楼层信息
            floor_info = info.xpath("./div[2]/div[2]/span[3]/text()").extract()
            # 建造时间
            build_time_info = info.xpath("./div[2]/div[2]/span[4]/text()").extract()
            # 经纪人姓名
            broker_name = info.xpath("./div[2]/div[2]/span[5]/text()").extract()
            # 地址
            address = info.xpath("./div[2]/div[3]/span/text()").extract()
            # 标签信息
            tags = []
            for tag in info.xpath("./div[2]/div[4]"):
                tag_str = tag.xpath("./span/text()").extract()
                tags.append(tag_str)
            # 价格
            price = info.xpath("./div[3]/span[1]/strong/text()").extract()
            # 每平米价格
            unit_price = info.xpath("./div[3]/span[2]/text()").extract()

            # 赋值到item对象上------------
            item['title'] = title[0].strip() if title else ''
            item['guarantee_info'] = guarantee_info[0] if guarantee_info else ''
            item['link'] = link[0] if link else ''
            item['house_type'] = house_type[0] if house_type else ''
            item['area'] = area[0] if area else ''
            item['floor_info'] = floor_info[0] if floor_info else ''
            item['build_time_info'] = build_time_info[0] if build_time_info else ''
            item['broker_name'] = broker_name[0] if broker_name else ''
            item['address'] = address[0].strip() if address else ''
            item['tags'] = tags[0] if tags else []
            item['price'] = price[0] if price else ''
            item['unit_price'] = unit_price[0] if unit_price else ''

            yield item


