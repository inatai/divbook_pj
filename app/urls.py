from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ItemView.as_view(), name='item'),
    path('item/<int:pk>/item_edit/', views.Item_editView.as_view(), name='item_edit'),
    path('item/item_add', views.item_add, name='item_add'),
    path('item/item_del/<int:pk>/', views.Item_del, name='item_del'),
    path('item/<int:pk>/calendar/', views.ItemCalendar.as_view(), name='calendar'),
    path('item/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.ItemCalendar.as_view(), name='calendar'),
    path('item/<int:pk>/booking/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Booking.as_view(), name='booking'),   
    path('item/<int:pk>/bookkk/<int:year>/<int:month>/<int:day>/<int:hour>/', views.bookkk, name='bookkk'), 
    path('item/<int:pk>/myschedule_detail/<int:year>/<int:month>/<int:day>/<int:hour>/', views.MyScheduleDetail.as_view(), name='myschedule_detail'),   
    path('item/myschedule_del/<int:pk>/', views.myschedule_del, name='myschedule_del'), 
    path('item/<int:pk>/rest/', views.Rest.as_view(), name='rest'),   
    path('item/<int:pk>/sendrest/', views.sendrest, name='sendrest'), 
    path('calendar/<int:pk>/my_page_calendar/', views.MyPageCalendar.as_view(), name='my_page_calendar'),
    path('calendar/<int:pk>/my_page_calendar/<int:year>/<int:month>/<int:day>/', views.MyPageCalendar.as_view(), name='my_page_calendar'),
    path('item/<int:pk>/config/<int:year>/<int:month>/<int:day>/', views.MyPageDayDetail.as_view(), name='my_page_day_detail'),#詳細
    path('item/holiday/add/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.my_page_holiday_add_hour, name='my_page_holiday_add_hour'),
    path('item/holiday/add/<int:pk>/<int:year>/<int:month>/<int:day>/', views.my_page_holiday_add_day, name='my_page_holiday_add_day'),
    path('item/delete_hour/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Delete_hour, name='delete_hour'),
    path('item/delete_day/<int:pk>/<int:year>/<int:month>/<int:day>/', views.Delete_day, name='delete_day'),
    path('item/eventcalendar/', views.EventcalendarView.as_view(), name='eventcalendar'),
    path('item/eventcalendar/<int:year>/<int:month>/', views.EventcalendarView.as_view(), name='eventcalendar'),
    path('item/event_add/', views.event_add, name='event_add'),
    path('item/some_event_add/', views.some_event_add, name='some_event_add'),
    path('item/event_del/<int:pk>/', views.event_del, name='event_del'),
    path('eventcalendar/<int:pk>/event_detail/', views.EventdetailView.as_view(), name='event_detail'),
    path('eventcalendar/<int:pk>/participant_add/', views.participant_add, name='participant_add'),
    path('eventcalendar/<int:pk>/<str:name>/participant_del/', views.participant_del, name='participant_del'),
    path('eventcalendar/<int:pk>/participant_detail/', views.ParticipantdetailView.as_view(), name='participant_detail'),
    path('eventcalendar/<int:pk>/my_participant_del/', views.my_participant_del, name='my_participant_del'),
]

app_name= 'app'