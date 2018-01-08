from urllib.parse import urlparse
import datetime


def remove_query_args(url):
    '''
    移除url链接中的get请求参数
    :param url:
    :return:
    '''
    o = urlparse(url)
    scheme = o.scheme
    netloc = o.netloc
    path = o.path
    return scheme + "://" + netloc + path


def now_timestamp():
    return datetime.datetime.now().timestamp()

def fmt_time(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    time = datetime.datetime.fromtimestamp(timestamp)
    return time.strftime(fmt)

def now_fmt_time():
    return fmt_time(now_timestamp())