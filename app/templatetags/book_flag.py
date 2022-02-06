from django import template

from django.utils import timezone
from datetime import datetime, date, timedelta, time


import datetime






register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.simple_tag
def book_start(start_day, event_date):
    flag = True
    today = datetime.date.today()
    book_start = event_date - datetime.timedelta(days=start_day)
    if today < book_start:
        flag = False
    
    return flag

@register.simple_tag
def book_end(end_day, event_date):
    flag = True
    today = datetime.date.today()
    book_end = event_date - datetime.timedelta(days=end_day)
    if today >= book_end:
        flag = False
    
    return flag

