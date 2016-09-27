# condig: utf-8

'''
レコメンド内容におけるモジュール
'''

import utils


class Module:
    '''
    処理の流れ
    入力データ -> 分析数値 -> レコメンド用数値・文章
    '''

    def __init__(self, rows_iter):
        '''
        [timestamp, value]のイテレータ rows_iter を受け取る
        '''
        self.rows_iter = rows_iter

    def _set_virtical_axis_values(self):
        '''
        グラフ用の値を生成するメソッド
        '''
        self.virtical_axis = []


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
    min_temp = 18
    max_temp = 30
    horizontal_axis_range = range(min_temp, max_temp + 1)
    horizontal_axis = [str(_) + "℃" for _ in horizontal_axis_range]

    def _set_virtical_axis_values(self):
        """
        各設定温度の使用頻度のリストを返す 単位は%
        # Return Example
        return [0, 0, 0, 0, 0, 0, 0, 30, 60, 10, 0, 0, 0]
        """
        count_list = [0] * len(self.horizontal_axis_range)
        for row in self.rows_iter:
            count_list[row.set_temperature - self.min_temp] += 1
        self.virtical_axis = [int((_ / sum(count_list) * 100)) for _ in count_list]

    # 以下アプリケーションメソッド
    def _find_frequent_set_temperature(self):
        '''
        データ解析部分
        1番頻繁に利用していた設定温度を返すメソッド
        '''
        return self.virtical_axis.index(max(self.virtical_axis)) + self.min_temp

    def _show_recommend_set_temperature(self, season="summer"):
        '''
        返す値部分
        設定を促すレコメンド設定温度を返すメソッド
        '''
        # TODO: Improve the recommend settemp function
        # TODO: 現在は推奨設定温度を頻繁利用温度から±2℃にしているので
        # プラスマイナスどのくらいが良いのかを詰めたものを
        # このモジュールにおけるデータ解析部分とする

        frequent_set_temp = self._find_frequent_set_temperature()
        if season == "summer":
            if 18 <= frequent_set_temp <= 28:
                return min(frequent_set_temp + 2, 28)
            elif frequent_set_temp > 28:
                return frequent_set_temp
            else:
                return frequent_set_temp
        elif season == "winter":
            if 20 <= frequent_set_temp <= 30:
                return max(frequent_set_temp - 2, 20)
            elif frequent_set_temp < 20:
                return frequent_set_temp
            else:
                return frequent_set_temp


class ReduceUsage(Module):
    '''
    利用時間削減に関するレコメンド
    1週間分におけるエアコン運転時間のグラフを持つ

    入力データ形式 : フィールド
    timestamp | on_off

    返り値データ形式
    * グラフ用データ
    * レコメンド用 エアコン削減可能曜日・その時間

    '''

    def _set_horizontal_axis_week_values(self):
        """
        # 日付の横軸ラベルを返す
        # Return Example
        # ["2016-08-14", "2016-08-15", "2016-08-16", "2016-08-17",
           "2016-08-18", "2016-08-19", "2016-08-20"]
        """
        ret_list = []
        dt = self.top_datetime
        for _ in range(7):
            insert_text = "{year}-{month}-{day}".\
                format(dt.year, month=dt.month, day=dt.day)
            ret_list.insert(0, insert_text)
            dt = utils.back_1day_ago(dt)
        self.horizontal_axis = ret_list

    def _set_virtical_axis_values(self, duration="weekly"):
        if duration == "weekly":
            self._set_virtical_axis_weekly_values()

    def _set_virtical_axis_weekly_values(self):
        """
        # 1週間分の各日におけるエアコン総稼働時間のリストを返す 単位はHour
        # Return Example
        #       日  月  火  水  木  金  土
        return [65, 59, 80, 81, 56, 55, 48]
        """

        # 1番始めのonから次に来るoffまでの時間の合計時間を求める
        # onの時の日にちをon->off間の日にちとする

        ret_list = [0] * 7
        on_operationg_flag = False
        index = 0
        for row in self.rows_iter:
            if row.on_off == "on" and not on_operationg_flag:
                on_operationg_flag = True

                on_timestamp = row.timestamp
                # examine on_timestamp's weekday
                weekday = on_timestamp.date().weekday()
                # convert weekday to ret_list index
                index = weekday + 1 if 0 <= weekday <= 5 else 0

            elif row.on_off == "off" and on_operationg_flag:
                on_operationg_flag = False

                off_timestamp = row.timestamp
                ret_list[index] += utils.make_delta_hour(on_timestamp,
                                                         off_timestamp)
        # 1番最後の日にちにおいて23:59まで分を合計に追加する
        if on_operationg_flag:
            days_last_timestamp = utils.make_days_last_timestamp(on_timestamp)
            ret_list[index] += utils.make_delta_hour(on_timestamp,
                                                     days_last_timestamp)

        self.virtical_axis = ret_list

    # 以下アプリケーションメソッド
    def find_the_rank_weekday(self, rank=1):
        '''
        指定のランクの曜日を返す
        '''
        weekday_rank_list = utils.make_ranking_index(self.virtical_axis)
        return utils.convert_num_to_weekday(weekday_rank_list[rank-1])


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

    # define specification of this graph
    horizontal_axis = [str(_) + ":00" for _ in range(24)]

    def _set_virtical_axis_values(self):
        """
        1週間分における時間当たりの使用率のリストを返す 単位は%
        # Return Example
        return [90, 19, 13, 32, 2, 12, 50, 90, 19, 13, 32, 2, 12, 50,
                90, 19, 13, 32, 2, 12, 50, 90, 19, 13, 32, 2, 12, 50]
        """
        count_list = [0] * len(self.horizontal_axis)
        on_operationg_flag = False
        for row in self.rows_iter:
            if row.on_off == "on" and not on_operationg_flag:
                on_operationg_flag = True
                on_timestamp = row.timestamp
            elif row.on_off == "off" and on_operationg_flag:
                on_operationg_flag = False
                off_timestamp = row.timestamp

                # on->off 期間のHourをカウントする
                over_days = off_timestamp.day - on_timestamp.day
                # 日をまたがないとき
                if over_days == 0:
                    for i in range(on_timestamp.hour, off_timestamp.hour + 1):
                        count_list[i] += 1
                # 日をまたぐとき
                else:
                    for i in range(on_timestamp.hour, 24):
                        count_list[i] += 1
                    for i in range(0, off_timestamp.hour + 1):
                        count_list[i] += 1

        if on_operationg_flag:
            for i in range(on_timestamp.hour, 24):
                count_list[i] += 1

        self.virtical_axis = [int(((_ / 7) * 100)) for _ in count_list]

    # 以下アプリケーションメソッド
    def find_a_certain_hour_value(self):
        """
        14時台での利用率を返すメソッド
        """
        a_certain_hour_index = 14  # 14:00での利用率が欲しい
        return self.virtical_axis[14]


if __name__ == "__main__":
    pass
