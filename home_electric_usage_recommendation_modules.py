# condig: utf-8

'''
レコメンド内容におけるモジュール
'''


class Module:
    '''
    処理の流れ
    入力データ -> 分析数値 -> レコメンド用数値・文章
    '''
    pass


class SettingTemp(Module):
    '''
    設定温度に関するレコメンド
    設定温度利用割合のグラフを持つ

    入力データ形式
    timestamp | set_temperature

    返り値データ
    * グラフ用データ
    * レコメンド用設定温度 <- これを示すことにおいては難しい機械学習は必要なさそう...

    '''
    pass


class ReduceUsage(Module):
    '''
    利用時間削減に関するレコメンド
    1週間分におけるエアコン運転時間のグラフを持つ

    入力データ形式
    timestamp | on_off

    返り値データ形式
    * グラフ用データ
    * レコメンド用 エアコン削減可能曜日・その時間

    '''
    pass


class ChangeUsage(Module):
    '''
    利用時間変更に関するレコメンド
    1日における時間帯ごとの利用割合のグラフを持つ

    入力データ形式
    timestamp | on_off

    返り値データ形式
    * グラフ用データ
    * レコメンド用 エアコン削減可能曜日・その時間

    '''
    pass


if __name__ == "__main__":
    pass
