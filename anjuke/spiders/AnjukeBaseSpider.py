import scrapy, json, os

from anjuke.items import AnjukeItem


def extract_house_id(link: str):
    '''
    从房屋链接中提取房屋id信息
    :param link:
    :return:
    '''
    link = link.strip()
    if link:
        r = link.split('?')[0].split('/')[-1]
        return r.strip()
    return ""


def extract_page_index(url: str):
    '''
    从当前url获取当前的页码信息
    :param url:
    :return:
    '''
    ol = str(url).split('/sale/')
    pnum = 1
    if len(ol) >= 2:
        sl = ol[1].split('/')
        if type(sl) != str and len(sl) >= 2:
            pnum = int(sl[1][1:])
    return pnum


cache_file = './tmp/cache_info.json'


def cache_crt_page_index(pnum):
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp', exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump({"crt_pnum": pnum}, f)


def load_crt_page_index_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_info = json.load(f)
            if 'crt_pnum' in cache_info:
                return cache_info.get("crt_pnum")
    return 0


class AnjukeBaseSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]
    page_index = 1

    def parse(self, response):

        print("开始解析第%s页 >>> " % self.page_index)
        crt_url = response.url
        print("当前url: {url}".format(url=crt_url))

        pnum = extract_page_index(crt_url)
        print(pnum)
        cache_crt_page_index(pnum)

        item = AnjukeItem()
        print('------------------------------------------------')
        info_list = response.xpath("//*[@id='houselist-mod-new']/li")
        for info in info_list:
            # 标题
            title = info.xpath("./div[2]/div[1]/a/text()").extract_first()
            # 安选验真信息
            guarantee_info = info.xpath("./div[2]/div[1]/em/@title").extract_first()
            # 链接
            link = info.xpath("./div[2]/div[1]/a/@href").extract_first()
            # 房屋id
            house_id = extract_house_id(link)
            # 户型
            house_type = info.xpath("./div[2]/div[2]/span[1]/text()").extract_first()
            # 面积
            area = info.xpath("./div[2]/div[2]/span[2]/text()").extract_first()
            # 楼层信息
            floor_info = info.xpath("./div[2]/div[2]/span[3]/text()").extract_first()
            # 建造时间
            build_time_info = info.xpath("./div[2]/div[2]/span[4]/text()").extract_first()
            # 经纪人姓名
            broker_name = info.xpath("./div[2]/div[2]/span[5]/text()").extract_first()
            # 地址
            address = info.xpath("./div[2]/div[3]/span/text()").extract_first()
            # 标签信息
            tags = []
            for tag in info.xpath("./div[2]/div[4]"):
                tag_str = tag.xpath("./span/text()").extract()
                tags.extend(tag_str)
            # 价格
            price = info.xpath("./div[3]/span[1]/strong/text()").extract_first()
            # 每平米价格
            unit_price = info.xpath("./div[3]/span[2]/text()").extract_first()

            # 赋值到item对象上------------
            item['house_id'] = house_id
            item['title'] = title.strip() if title else ''
            item['guarantee_info'] = guarantee_info if guarantee_info else ''
            item['link'] = link if link else ''
            item['house_type'] = house_type if house_type else ''
            item['area'] = area if area else ''
            item['floor_info'] = floor_info if floor_info else ''
            item['build_time_info'] = build_time_info if build_time_info else ''
            item['broker_name'] = broker_name if broker_name else ''
            item['address'] = address.strip() if address else ''
            item['tags'] = tags if tags else []
            item['price'] = price if price else ''
            item['unit_price'] = unit_price if unit_price else ''
            yield item

        # 下一页地址
        next_page_url = response.xpath("//*[@id='content']/div[4]/div[7]/a[@class='aNxt']/@href").extract_first()
        print(next_page_url)
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

        self.page_index += 1
