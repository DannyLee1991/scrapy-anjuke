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


class AnjukeShanghaiListSaleSpider(AnjukeBaseSpider):
    name = "anjuke_shanghai"

    # 所有一级行政区
    # area_list = ['pudong', 'minhang', 'baoshan', 'xuhui', 'songjiang', 'jiading', 'putuo', 'yangpu', 'hongkou',
    #              'changning', 'huangpu', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian']

    # 所有二级行政区
    area_list = ['weifang', 'kangqiao', 'yangsi', 'xinchang', 'shibo', 'yuanshen', 'jinyang', 'sanlin',
                 'lingangxincheng', 'gaoxing', 'yuqiao', 'huamu', 'shuyuan', 'beicai', 'huinan', 'zhoupu', 'datuan',
                 'waigaoqiao', 'tangqiao', 'jinqiao', 'nicheng', 'lujiazui', 'yangjing', 'tangzhen', 'caolu', 'biyun',
                 'gaodong', 'sanlinnan', 'chuansha', 'shijigongyuan', 'luchaogang', 'hangtou', 'nanmatou', 'zhangjiang',
                 'sunqiao', 'yangdong', 'lianyang', 'wanxiang', 'laogang', 'zhangjiang(dong)', 'xuanqiao', 'heqing',
                 'pudongjichang', 'gumei', 'pujiangzhen', 'xinzhuang', 'zhuanqiao', 'laominxing', 'maqiao',
                 'longbaijinhui', 'huacao', 'meilong', 'qibao', 'jinhongqiao', 'chunshen', 'gubei(minxing)',
                 'jinganxincheng', 'hanghua', 'wujing', 'xujing', 'zhaoxiang', 'xianghuaqiao', 'baihe', 'zhujiajiao',
                 'qingpuxincheng', 'huaxin', 'jinze', 'zhonggu', 'kunshan', 'jiaxing', 'nantong', 'suzhou', 'huzhou',
                 'cixi', 'xintiandi', 'shibobinjiang', 'dapuqiao', 'fuxinggongyuan', 'wuliqiao', 'yuyuan',
                 'nanjingdonglu', 'penglaigongyuan', 'laoximen', 'huangpubinjiang', 'dongjiadu', 'renminguangchang',
                 'jiadinglaocheng', 'jiangqiao', 'anting', 'waigang', 'jiadingbei', 'jiadingxincheng', 'nanxiang',
                 'fengzhuang', 'huating', 'malu', 'juyuanxinqu', 'nanxiangxincheng', 'fangtai', 'caowang', 'jianbang',
                 'fengbang', 'daning', 'jiangninglu', 'caojiadu', 'beijiaozhan', 'dayuecheng', 'xizangbeilu', 'yonghe',
                 'zhabeigongyuan', 'nanjingxilu', 'xinkezhan', 'pengpu', 'jingansi', 'luodian', 'yangxing', 'dahua',
                 'songbao', 'tonghe', 'gongkang', 'gongfu', 'luojing', 'gucun', 'shangda', 'songnan', 'yuepu',
                 'gaojing', 'baochengonglu', 'dachang', 'longhua', 'huajing', 'zhangqiao', 'kangjian', 'xujiahui',
                 'huadongligong', 'hongmeilu', 'wantiguan', 'tianlin', 'xuhuibinjiang', 'xietulu', 'zhiwuyuan',
                 'shanghainanzhan', 'jianguoxilu', 'hengshanlu', 'caohejing', 'shenminbieshuqu', 'sheshan', 'chedun',
                 'songjianglaocheng', 'sijing', 'songjiangxincheng', 'jiuting', 'songjiangdaxuecheng',
                 'songjiangquqita', 'yexie', 'xinqiao', 'maogang', 'dongjing', 'zhangfeng', 'ganquanyichuan',
                 'changzheng', 'liziyuan', 'wanli', 'taopu', 'guangxin', 'zhenru', 'changshou', 'caoyang', 'zhenguang',
                 'wuning', 'zhongyuanliangwancheng', 'yangguangweinisi', 'yangpudaqiao', 'dongwaitan',
                 'huangxinggongyuan', 'wujiaochang', 'kongjianglu', 'anshan', 'zhongyuan', 'wujiaochangbei',
                 'zhangbaixincun', 'jiangpulu', 'xinjiangwancheng', 'sichuanbeilu', 'linpinglu', 'liangcheng',
                 'guangzhonglu', 'quyang', 'luxungongyuan', 'dabaishu', 'jiangwanzhen', 'beiwaitan', 'hepinggongyuan',
                 'zhongshangongyuan', 'beixinjing', 'xinhualu', 'gubei', 'tianshan', 'xijiao', 'xianxia', 'hongqiao',
                 'hongqiaojichang', 'situan', 'jinhui', 'pingan', 'qingcunbei', 'nanqiao', 'fengcheng', 'haiwan',
                 'zhelin', 'zhuangxing', 'qingcunnan', 'xidu', 'tinglin', 'shihua', 'shanyang', 'zhujing', 'zhangyan',
                 'fengjing', 'caojing', 'zhuxing', 'langxia', 'lvxiang', 'changxingdao', 'chongmingzhucheng',
                 'hengshadao']

    print("开始生成起始url")
    start_urls = gen_start_urls(area_list)
    print("开始爬取")
