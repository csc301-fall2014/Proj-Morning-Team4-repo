from scheduler.models import Calendar, Event
from django.contrib.auth.models import User
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker



class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'start', 'end', 'location')
        widgets = {
        	'name': forms.TextInput(attrs={'class': 'form-control'}),
        	'description': forms.TextInput(attrs={'class': 'form-control'}),
        	'start': DateTimePicker(attrs={'class': 'form-control'},options={
        		'format': "MM/DD/YYYY HH:mm",
        		}),
        	'end': DateTimePicker(attrs={'class': 'form-control'},options={
        		'format': "MM/DD/YYYY HH:mm",
        		}),
        	'location': forms.TextInput(attrs={'class': 'form-control'}),

        }
        
