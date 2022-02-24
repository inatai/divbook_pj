# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from app.models import Item, Schedule, Event, Participant
from datetime import datetime,timedelta
from django.utils.timezone import make_aware
from django.db.models import Q
 
from email.mime.text import MIMEText
import smtplib
import sys
import os
import logging
 
#初期パラメータ設定
# logdir = "app/logfile/"
 
 
#現在時刻の取得
# date_name = datetime.now().strftime("%Y%m%d-%H%M%S")
 
#ファイル名の生成
# file_name = logdir + date_name + "_" + "LOTATE_PERF_HIST_PY.log"
# logging.basicConfig(filename=file_name,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
 
 
class Command(BaseCommand):
 
    """ カスタムコマンド定義 """
 
    def handle(self, *args, **options):
 
        # ここに実行したい処理を書く
        # logging.info('[正常]パフォーマンス履歴データのハウスキープ処理を開始。')
 
        try:
            import datetime
            d_todatetime = make_aware(datetime.datetime.today() )  #現在日付の取得
            before_60_datetimes = d_todatetime - timedelta(days=60)   #60日前の日付を取得

            Schedule.objects.filter(Q(start__lt=before_60_datetimes)).delete()   #60前のレコードを抽出して削除
            Event.objects.filter(Q(date__lt = before_60_datetimes)).delete()
 
 
        except Exception as e:
            # logging.info('[異常]パフォーマンス履歴データのハウスキープ処理でエラーが発生しました。')
            # logging.info('[異常]エラー内容:%s', str(e.args))
            # logging.exception('Detail: %s', e)
            # logging.info('[異常]パフォーマンス履歴データのハウスキープ処理が異常終了しました。')

            sys.exit(1)
 
        # logging.info('[正常]パフォーマンス履歴データのハウスキープ処理が正常終了しました。')