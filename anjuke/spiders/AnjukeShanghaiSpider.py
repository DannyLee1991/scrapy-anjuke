from anjuke.spiders.AnjukeBaseSpider import AnjukeBaseSpider


class AnjukeShanghaiSpider(AnjukeBaseSpider):
    name = "anjuke_shanghai"

    start_urls = [
        'https://shanghai.anjuke.com/sale/',
        'https://shanghai.anjuke.com/sale/pudong/',
        'https://shanghai.anjuke.com/sale/minhang/',
        'https://shanghai.anjuke.com/sale/baoshan/',
        'https://shanghai.anjuke.com/sale/xuhui/',
        'https://shanghai.anjuke.com/sale/songjiang/',
        'https://shanghai.anjuke.com/sale/jiading/',
        'https://shanghai.anjuke.com/sale/jingan/',
        'https://shanghai.anjuke.com/sale/putuo/',
        'https://shanghai.anjuke.com/sale/yangpu/',
        'https://shanghai.anjuke.com/sale/hongkou/',
        'https://shanghai.anjuke.com/sale/changning/',
        'https://shanghai.anjuke.com/sale/huangpu/',
        'https://shanghai.anjuke.com/sale/qingpu/',
        'https://shanghai.anjuke.com/sale/fengxian/',
        'https://shanghai.anjuke.com/sale/jinshan/',
        'https://shanghai.anjuke.com/sale/chongming/',
        'https://shanghai.anjuke.com/sale/shanghaizhoubian/',
    ]
