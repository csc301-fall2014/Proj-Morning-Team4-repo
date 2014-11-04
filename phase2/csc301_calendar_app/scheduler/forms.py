from scheduler.models import Calendar, Event
from django.contrib.auth.models import User
from django import forms


class EventForm(forms.ModelForm):

    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    start = forms.DateTimeField(widget=forms.DateTimeInput(), required=True)
    end = forms.DateTimeField(required=False)
    location = forms.CharField(required=True)

    class Meta:
        model = Event
        fields = ('name', 'description', 'start', 'end', 'location')
