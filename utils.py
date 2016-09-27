# condig: utf-8


def make_ranking_index(vlist):
    '''
    指定の配列におけるランキングをインデックス基準に返す
    >>> find_top1_weekday([19, 21, 11, 38, 21, 13, 28])
    [3, 6, 1, 4, 0, 5, 2]
    '''
    dic = {}
    for i, v in enumerate(vlist):
        dic.setdefault(v, []).append(i)
    ret = []
    for k, v in reversed(sorted(dic.items())):
        while v:
            ret.append(v.pop(0))
    return ret


def convert_num_to_weekday(num):
    '''
    曜日インデックスを日本語に変換するメソッド
    >>> convert_num_to_weekday(2)
    '火'
    '''
    convert_list = ["日", "月", "火", "水", "木", "金", "土"]
    return convert_list[num]
