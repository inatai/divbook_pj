from django import forms
from .models import  Item, Event


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', 'description')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'book_start', 'book_end', 'limit')