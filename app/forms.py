from dataclasses import field
from mimetypes import init
from pdb import post_mortem
from django import forms
from django.utils import timezone
from .models import Schedule, Item, Event


class BookForm(forms.Form):
    name = forms.CharField(max_length=30, label='予約者名')
    start = forms.DateTimeField(
        label='開始時刻',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )
    end = forms.DateTimeField(
        label='終了時間',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True
    )
    
    def save(self):
        data = self.cleaned_data
        schedule = Schedule(name=data['name'], start=data['start'], end=['end'])
        schedule.save()

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', 'description')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'book_start', 'book_end')