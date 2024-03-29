# Generated by Django 4.0.1 on 2022-02-06 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='表示名')),
                ('description', models.TextField(blank=True, default='特になし', verbose_name='備考等')),
                ('date', models.DateField(verbose_name='開催日')),
                ('book_start', models.IntegerField(verbose_name='予約開始日数')),
                ('book_end', models.IntegerField(verbose_name='予約締め切り日数')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='表示名')),
                ('description', models.TextField(blank=True, default='特になし', verbose_name='備考等')),
                ('deadline', models.IntegerField(blank=True, default='30', verbose_name='期限(日)')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item', verbose_name='モノ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='スタッフ')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='開始時間')),
                ('name', models.CharField(max_length=255, verbose_name='予約者名')),
                ('pw', models.CharField(max_length=4, verbose_name='暗証番号')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='予約者名')),
                ('pw', models.CharField(max_length=4, verbose_name='暗証番号')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event')),
            ],
        ),
    ]
