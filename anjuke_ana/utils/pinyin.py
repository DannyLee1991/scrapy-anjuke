from pypinyin import pinyin, lazy_pinyin


def get_pinyin(txt):
    return lazy_pinyin(txt)


if __name__ == '__main__':
    from anjuke_ana.db.read_data import get_all_locate_a, get_all_locate_b

    l = []
    for locate_a in get_all_locate_a():
        # print(locate_a)
        for locate_b in get_all_locate_b(locate_a):
            # print("     " + locate_b)
            l.append("".join(get_pinyin(locate_b)))
    # r = get_pinyin("你好")
    print(l)
