from scrapy.crawler import CrawlerProcess
from anjuke.spiders.AnjukeShanghaiSpider import AnjukeShanghaiSpider


if __name__ == '__main__':
    # 创建一个CrawlerProcess对象
    process = CrawlerProcess()  # 括号中可以添加参数

    process.crawl(AnjukeShanghaiSpider)
    process.start()
