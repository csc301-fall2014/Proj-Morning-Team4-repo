from school.models import SchoolProfile
from django import forms
from main.models import UserProfile
from django.contrib.auth.models import User


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('school',)
