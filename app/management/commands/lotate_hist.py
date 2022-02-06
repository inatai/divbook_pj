# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from app.models import Schedule, Event
from datetime import datetime,timedelta

from email.mime.text import MIMEText
import smtplib
import sys
import os
import logging

#初期パラメータ設定
logdir = "app/logfile/"


#現在時刻の取得
date_name = datetime.now().strftime("%Y%m%d-%H%M%S")

#ファイル名の生成
file_name = logdir + date_name + "_" + "LOTATE_PERF_HIST_PY.log"
logging.basicConfig(filename=file_name,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class Command(BaseCommand):

    """ カスタムコマンド定義 """

    def handle(self, *args, **options):

        # ここに実行したい処理を書く
        logging.info('[正常]パフォーマンス履歴データのハウスキープ処理を開始。')

        try:
            import datetime
            d_today = datetime.date.today()   #現在日付の取得
            before_1_days = d_today - timedelta(days=1)   #1日前の日付を取得
            Schedule.objects.filter(update_time__lte=before_1_days).delete()   #1前のレコードを抽出して削除
            Event.objects.filter(update_time__lte=before_1_days).delete()   #1前のレコードを抽出して削除


        except Exception as e:
            logging.info('[異常]パフォーマンス履歴データのハウスキープ処理でエラーが発生しました。')
            logging.info('[異常]エラー内容:%s', str(e.args))
            logging.exception('Detail: %s', e)
            logging.info('[異常]パフォーマンス履歴データのハウスキープ処理が異常終了しました。')
            sys.exit(1)

        logging.info('[正常]パフォーマンス履歴データのハウスキープ処理が正常終了しました。')