from calendar import weekday
from distutils.log import error
from email.mime import base
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from . import forms
from .models import Item, Schedule, Event, Participant
from django.utils import timezone
from datetime import datetime, date, timedelta, time

from django.views import generic
from django.db.models import Q
from django.contrib import messages
import datetime
from django.contrib.auth.mixins import  LoginRequiredMixin, UserPassesTestMixin


from .forms import ItemForm, EventForm

from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from django.views.decorators.clickjacking import xframe_options_exempt

from django import forms

ScheduleFormSet = forms.modelformset_factory(Schedule, fields='__all__', can_delete=True, extra=0)

# Create your views here.

class ItemView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.all()

        return render(request, 'app/item.html',{
            'item_data': item_data
        })
    

#受付の追加
def item_add(request):
    if LoginRequiredMixin:
        form = ItemForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                item = Item()
                print(request)
                item.name = request.POST['name']
                item.description = request.POST['description']
                # item.image = request.FILES['image']
                item.save()
                return redirect('app:item')
            else:
                form = ItemForm()

    return render(request, 'app/item_add.html', {'form': form})


#受付の消去
@require_POST
def Item_del(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if LoginRequiredMixin:
        item_data = Item.objects.filter(pk=pk)

        item_data.delete()

    return redirect('app:item')

#カレンダー表示
class ItemCalendar(generic.TemplateView):
    template_name = 'app/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 0時から23時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(0, 24):
            row = {}
            for day in days:
                row[day] = []
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=0, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=23, minute=0, second=0))
        for schedule in Schedule.objects.filter(item=item).exclude(Q(start__gt=end_time) | Q(start__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date].append(schedule)

        context['item'] = item
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        return context

#予約フォーム表示
class Booking(generic.CreateView):
    model = Schedule
    fields = ('name',)
    template_name = 'app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = get_object_or_404(Item, pk=self.kwargs['pk'])
        return context
#予約の送信
@require_POST
def bookkk(request, pk, year, month, day, hour):
    get_number = request.POST.get('number')
    get_name = request.POST.get('name')
    get_pw = request.POST.get('pw')
    get_number = int(get_number)
    
   

    item = get_object_or_404(Item, pk=pk)
    today = datetime.date.today()

    start = datetime.datetime(year=year, month=month, day=day, hour=hour)

    flag = True
    for h in range(0, get_number):
        if Schedule.objects.filter(item=item, start=start+timedelta(hours=h)).exists():
                messages.error(request, '既に予約があります。')
                flag = False
                break
    if(flag):
        for h in range(0, get_number):
            start_d = start + timedelta(hours=h)
            Schedule.objects.create(item=item, start=start_d, name=get_name, pw = get_pw) 
    
        messages.success(request, '予約が完了しました')
    
    return redirect('app:calendar', pk=pk, year=today.year, month=today.month, day=today.day)
    

#一括休暇設定ページ表示
class Rest(LoginRequiredMixin, generic.CreateView):
    model = Schedule
    fields = ('name',)
    template_name = 'app/rest.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = get_object_or_404(Item, pk=self.kwargs['pk'])
        return context

#一括休暇送信
@require_POST
def sendrest(request, pk):
    get_start = request.POST.get('start')
    get_end = request.POST.get('end')
    get_weeklist = request.POST.getlist('weeks') 
    
    startlist = get_start.split('-')
    endlist = get_end.split('-')
    start = datetime.datetime(year=int(startlist[0]), month=int(startlist[1]), day=int(startlist[2]), hour=0)
    end = datetime.datetime(year=int(endlist[0]), month=int(endlist[1]), day=int(endlist[2]), hour=0)
    today = datetime.date.today()
    
    if(start>end):
        messages.error(request, '日付の入力が正しくありません。')
        
    else:
        for i in range((end - start).days + 1):
            date = (start + timedelta(i))
            if(str(date.weekday()) in get_weeklist):
                my_page_holiday_add_day(request=request, pk=pk, year=date.year, month=date.month, day=date.day)
    
    return redirect('app:my_page_calendar', pk=pk, year=today.year, month=today.month, day=today.day)


#スタッフ用カレンダーページ表示
class MyPageCalendar(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app/my_page_calender.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 0時から23時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(0, 24):
            row = {}
            for day in days:
                row[day] = []
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=0, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=23, minute=0, second=0))
        for schedule in Schedule.objects.filter(item=item).exclude(Q(start__gt=end_time) | Q(start__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date].append(schedule)

        context['item'] = item
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        return context


#カレンダー詳細ページ表示
class MyPageDayDetail(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app/my_page_day_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        item = get_object_or_404(Item, pk=pk)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.date(year=year, month=month, day=day)

        # 0時から24時まで1時間刻みのカレンダーを作る
        calendar = {}
        for hour in range(0, 24):
            calendar[hour] = []

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(date, datetime.time(hour=0, minute=0, second=0))
        end_time = datetime.datetime.combine(date, datetime.time(hour=23, minute=0, second=0))
        for schedule in Schedule.objects.filter(item=item).exclude(Q(start__gt=end_time) | Q(start__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar:
                calendar[booking_hour].append(schedule)

        context['calendar'] = calendar
        context['item'] = item
        return context


#スケジュール詳細ページ表示
class MyScheduleDetail(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app/myschedule_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        item = get_object_or_404(Item, pk=pk)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        dt = datetime.datetime(year=year, month=month, day=day, hour=hour)

        schedule = get_object_or_404(Schedule, item=item, start=dt)

        if(schedule.pw == ''):
            flag = False
        else:
            flag = True

        context['item'] = item
        context['schedule'] = schedule
        context['flag'] = flag
        
        return context

@require_POST
def myschedule_del(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    dt = schedule.start
    item =schedule.item
    get_pw = request.POST.get('pw')
    get_number = request.POST.get('number')
    get_number = int(get_number)

    flag = True
    #予約の有無を確認
    for n in range(0, get_number):
        if Schedule.objects.filter(item=item, start=dt+timedelta(hours=n)).exists():
            sc = get_object_or_404(Schedule, item=item, start=dt+timedelta(hours=n))
            if(sc.pw != get_pw):
                flag = False
                messages.error(request, '暗証番号が一致しない時間帯があります。')
                break
        else:
            flag = False
            messages.error(request, '予約がない時間帯が指定されています。')
            break
    #予約の確認が取れたら消去   
    if(flag):
        for n in range(0, get_number):
            sc = Schedule.objects.filter(item=item, start=dt+timedelta(hours=n))
            sc.delete()
        return redirect('app:calendar', pk=item.pk)
    else:
        adt = dt + timedelta(hours=9)
        print(adt)
        print("じかん")
        return redirect('app:myschedule_detail', pk=item.pk, year=adt.year, month=adt.month, day=adt.day, hour=adt.hour)


@require_POST
def Delete_hour(request, pk, year, month, day, hour):
    item = get_object_or_404(Item, pk=pk)
    if LoginRequiredMixin:
        start_time = datetime.datetime(year=year, month=month, day=day, hour=hour)
        booking_data = Schedule.objects.filter(start=start_time)

        booking_data.delete()

    today = datetime.date.today()
    return redirect('app:my_page_calendar', pk=pk, year=today.year, month=today.month, day=today.day)

@require_POST
def Delete_day(request, pk, year, month, day):
    item = get_object_or_404(Item, pk=pk)
    if LoginRequiredMixin:
        for h in range(0, 24):
            start_time = datetime.datetime(year=year, month=month, day=day, hour=0)+timedelta(hours=h)
            booking_data = Schedule.objects.filter(start=start_time)
            booking_data.delete()

    today = datetime.date.today()
    
    return redirect('app:my_page_calendar', pk=pk, year=today.year, month=today.month, day=today.day)


@require_POST
def my_page_holiday_add_hour(request, pk, year, month, day, hour):
    item = get_object_or_404(Item, pk=pk)
    if LoginRequiredMixin:
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        Schedule.objects.create(item=item, start=start, name='予約不可')
        return redirect('app:my_page_day_detail', pk=pk, year=year, month=month, day=day)

    raise PermissionDenied

@require_POST
def my_page_holiday_add_day(request, pk, year, month, day):
    item = get_object_or_404(Item, pk=pk)

    start = datetime.datetime(year=year, month=month, day=day, hour=0)

    if LoginRequiredMixin:
        flag = True
        for h in range(0, 24):
            if Schedule.objects.filter(item=item, start=start+timedelta(hours=h)).exists():
                    messages.error(request, '既に予約があります。')
                    flag = False
                    break
        if(flag):
            for h in range(0, 24):
                start_d = start+timedelta(hours=h)
                Schedule.objects.create(item=item, start=start_d, name='予約不可')
        today = datetime.date.today()
        return redirect('app:my_page_calendar', pk=pk, year=today.year, month=today.month, day=today.day)
    raise PermissionDenied


class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class EventcalendarView(XFrameOptionsExemptMixin, generic.TemplateView):
    template_name = 'app/eventcalendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        if year and month:
            base_date = datetime.date(year=year, month=month, day=1)
        else:
            base_date = today.replace(day=1)

        first_day = base_date

        #basedateを月曜日に調整
        for n in range(0, 7):
            date = base_date - datetime.timedelta(days=n)
            if(date.weekday() == 0):
                first_day = date
                break

        days = [first_day + datetime.timedelta(days=day) for day in range(35)]
        
        if(days[-1].month == base_date.month):
            days = [first_day + datetime.timedelta(days=day) for day in range(42)]
            syu = 6
        else:
            syu = 5

        split_days = []
        #配列の要素数をカウント
        length = len(days)
        #配列を指定した個数で分割していくループ処理
        s = 7 #何個ずつ分割
        n = 0 #開始位置
        for i in days:
            split_days.append(days[n:n+s:1])
            n += s
            #カウント数が配列の長さを超えたらループ終了
            if n >= length:
                break

        start_day = days[0]
        end_day = days[-1]
        weeks = [0, 1, 2, 3, 4, 5, 6]
        week_name = ["月","火","水","木","金","土","日"]

        x = 0
        calendar = {}
        for n in range(0, syu):     
            for w in weeks:
                d = split_days[n][w]
                x =n*7+(w+1)
                row = {}
                row[x-1] = []
                calendar[d] = row
        #calendar[日付][週の番号]
        
        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        for event in Event.objects.exclude(Q(date__gt=end_day) | Q(date__lt=start_day)):
            event_date = event.date
            n = (event_date - start_day).days
            calendar[event_date][n].append(event)
            

        if base_date.month == 12:
            next_month = base_date.replace(year=base_date.year+1, month=1)
        else:
            next_month = base_date.replace(month=base_date.month + 1)
        if base_date.month == 1:
            before_month = base_date.replace(year=base_date.year-1, month=12)
        else:
            before_month = base_date.replace(month=base_date.month - 1)

        context['month'] = base_date.month
        context['now_month_f'] = base_date.replace(year=base_date.year, month=base_date.month, day=1)
        context['now_month_e'] = (base_date.replace(year=base_date.year, month=base_date.month+1, day=1)) - datetime.timedelta(days=1)
        
        context['calendar'] = calendar
        context['days'] = days
        context['week_name'] = week_name
        context['weeks'] = weeks
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['next'] = next_month
        context['before'] = before_month
        context['today'] = today

        return context

# class EventcalendarView(XFrameOptionsExemptMixin, generic.TemplateView):
#     template_name = 'app/eventcalendar.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today = datetime.date.today()
#         # event = Event.objects.all()
 
#         # どの日を基準にカレンダーを表示するかの処理。
#         # 年月日の指定があればそれを、なければ今日からの表示。
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         day = self.kwargs.get('day')
#         if year and month and day:
#             base_date = datetime.date(year=year, month=month, day=day)
#         else:
#             base_date = today

#         # カレンダーは1ヶ月分表示するので、基準日からの日付を作成しておく
#         days = [base_date + datetime.timedelta(days=day) for day in range(7)]
#         start_day = days[0]
#         end_day = days[-1]

#         # 0時から23時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
#         calendar = {}
#         for day in days:
#             calendar[day] = []

#         # カレンダー表示する最初と最後の日時の間にある予約を取得する
#         for event in Event.objects.exclude(Q(date__gt=end_day) | Q(date__lt=start_day)):
#             local_dt = event.date
#             booking_date = local_dt

#             if booking_date in calendar:
#                 calendar[booking_date].append(event)

#         context['calendar'] = calendar
#         context['days'] = days
#         context['start_day'] = start_day
#         context['end_day'] = end_day
#         context['before'] = days[0] - datetime.timedelta(days=7)
#         context['next'] = days[-1] + datetime.timedelta(days=1)
#         context['today'] = today
#         return context


#受付の追加
def event_add(request):
    if LoginRequiredMixin:
        form = EventForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                event = Event()
                event.name = request.POST['name']
                event.description = request.POST['description']
                event.book_start = int(request.POST['book_start'])-1
                event.book_end = int(request.POST['book_end'])-1

                #1日だけ追加
                if event.book_start < event.book_end:
                    messages.error(request, '予約期限の入力が正しくありません。')
                    return redirect('app:event_add')

                elif(request.POST.get('date')):
                    get_date = request.POST.get('date')
                    datelist = get_date.split('-')
                    event.date = datetime.date(year=int(datelist[0]), month=int(datelist[1]), day=int(datelist[2]))
                    event.save()
                    return redirect('app:item')

                else:
                    messages.error(request, '入力が正しくありません')
                    return redirect('app:event_add')

            else:
                form = EventForm()
    return render(request, 'app/event_add.html', {'form': form})


def some_event_add(request):
    if LoginRequiredMixin:
        form = EventForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                event = Event()
                event.name = request.POST['name']
                event.description = request.POST['description']
                event.book_start = int(request.POST['book_start'])-1
                event.book_end = int(request.POST['book_end'])-1

                get_name = request.POST['name']
                get_description = request.POST['description']
                get_book_start = int(request.POST['book_start'])-1
                get_book_end = int(request.POST['book_end'])-1

                #まとめて追加
                if event.book_start < event.book_end:
                    messages.error(request, '予約期限の入力が正しくありません。')
                    return redirect('app:some_event_add')

                elif(request.POST.get('start') and request.POST.get('end')):
                    get_start = request.POST.get('start')
                    get_end = request.POST.get('end')
                    get_weeklist = request.POST.getlist('weeks')       
                    startlist = get_start.split('-')
                    endlist = get_end.split('-')
                    start = datetime.date(year=int(startlist[0]), month=int(startlist[1]), day=int(startlist[2]))
                    end = datetime.date(year=int(endlist[0]), month=int(endlist[1]), day=int(endlist[2]))
     
                    if(start>=end):
                        messages.error(request, '日付の入力が正しくありません。')
                        return redirect('app:some_event_add')
                    else:
                        for i in range((end - start).days + 1):
                            date = (start + timedelta(i))
                            if(str(date.weekday()) in get_weeklist):
                                event.date = date
                                Event.objects.create(name=get_name, date=date, book_start=get_book_start, 
                                book_end=get_book_end, description=get_description)
                        return redirect('app:item')
                else:
                    messages.error(request, '入力が正しくありません')
                    return redirect('app:some_event_add')

            else:
                form = EventForm()
    return render(request, 'app/some_event_add.html', {'form': form})


#受付の消去
@require_POST
def event_del(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if LoginRequiredMixin:
        event.delete()

    return redirect('app:item')



class EventdetailView(generic.TemplateView):
    template_name = 'app/event_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        today = datetime.date.today()
        date = event.date
        book_start = date - datetime.timedelta(days=event.book_start)
        book_end = date - datetime.timedelta(days=event.book_end)

        context['event'] = event
        context['today'] = today
        context['book_start'] = book_start
        context['book_end'] = book_end

        #予約者一覧
        pa_list = {}
        n = 1
        for participant in Participant.objects.filter(event=event).all():
            pa_list.setdefault(n, participant)
            n+=1
        context['participants'] = pa_list

        return context

@require_POST
def participant_add(request, pk):
    event = get_object_or_404(Event, pk=pk)
    name = request.POST.get('name')
    pw = request.POST.get('pw')
    if Participant.objects.filter(event=event, name=name):
        messages.error(request, '同名の予約があります。漢字やカタカタ等を使用して違う名前で予約してください。')
    else:
        Participant.objects.create(event=event, name=name, pw=pw)
        messages.success(request, '予約が完了しました')

    return redirect('app:event_detail', pk=pk)

@require_POST
def participant_del(request, pk, name):
    event = get_object_or_404(Event, pk=pk)
    name = name
    if LoginRequiredMixin:
        participant_data = Participant.objects.filter(event=event, name=name)
        participant_data.delete()
    
    return redirect('app:event_detail', pk=pk)

class ParticipantdetailView(generic.TemplateView):
    template_name = 'app/participant_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participant = get_object_or_404(Participant, pk=self.kwargs['pk'])
        event = participant.event
        date = event.date

        flag = True
        if(participant.pw == ''):
            flag = False

        context['event'] = event
        context['date'] = date
        context['participant'] = participant
        context['flag'] = flag

        return context

@require_POST
def my_participant_del(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    event = participant.event
    
    pw = request.POST.get('pw')
    if(participant.pw == pw):
        participant.delete()
        messages.error(request, '予約をキャンセルしました。')
    else:
        messages.error(request, 'パスワードが一致しません。')
        
    return redirect('app:event_detail', pk = event.pk)
    