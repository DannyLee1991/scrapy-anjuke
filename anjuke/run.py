from scrapy.crawler import CrawlerProcess
from anjuke.spiders.AnjukeShanghaiSpider import AnjukeShanghaiSpider
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    # 创建一个CrawlerProcess对象
    process = CrawlerProcess(settings=get_project_settings())  # 括号中可以添加参数

    process.crawl(AnjukeShanghaiSpider)
    process.start()
