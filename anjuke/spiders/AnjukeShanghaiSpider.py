from anjuke.spiders.AnjukeBaseSpider import AnjukeBaseSpider, load_crt_page_index_cache


def gen_start_urls(area_list):
    '''
    生成起始url
    :param area_list:
    :return:
    '''
    start_urls = ['https://shanghai.anjuke.com/sale/', ]

    for area in area_list:
        start_url = "https://shanghai.anjuke.com/sale/{area}/".format(area=area)
        start_urls.append(start_url)

    # 使用缓存数据
    crt_page_index = load_crt_page_index_cache()
    if crt_page_index != 0:
        for i in range(len(start_urls)):
            start_urls[i] += "p{num}".format(num=crt_page_index)

    return start_urls


class AnjukeShanghaiSpider(AnjukeBaseSpider):
    name = "anjuke_shanghai"

    area_list = ['pudong', 'minhang', 'baoshan', 'xuhui', 'songjiang', 'jiading', 'putuo', 'yangpu', 'hongkou',
                 'changning', 'huangpu', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian']

    print("开始生成起始url")
    start_urls = gen_start_urls(area_list)
    print("开始爬取")
