from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

# Create your models here.


class Item(models.Model):
    name = models.CharField('表示名',max_length=100)
    description = models.TextField('備考等', default='特になし', blank=True)
    deadline = models.IntegerField('期限(日)', default='30', blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField('表示名',max_length=100)
    description = models.TextField('備考等', default='特になし', blank=True)
    date = models.DateField('開催日')
    book_start = models.IntegerField('予約開始日数')
    book_end = models.IntegerField('予約締め切り日数')

    def __str__(self):
        return self.name


class Staff(models.Model):#ユーザー情報とアイテムを1対1で結びつける
    #user = models.CharField('スタッフ', max_length=100)
    user = models.OneToOneField(CustomUser, verbose_name='スタッフ', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='モノ', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item}:{self.user}'


class Schedule(models.Model):
    start = models.DateTimeField('開始時間')
    name = models.CharField('予約者名', max_length=255)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    pw = models.CharField('暗証番号', max_length=4)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.name} {start}'

class Participant(models.Model):
    name = models.CharField('予約者名', max_length=255)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    pw = models.CharField('暗証番号', max_length=4)

    def __str__(self):
        return f'{self.name}'