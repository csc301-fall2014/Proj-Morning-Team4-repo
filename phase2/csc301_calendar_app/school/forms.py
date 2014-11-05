from school.models import SchoolProfile, Course
from django import forms
from main.models import Student
from django.contrib.auth.models import User


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('school',)


class CourseForm(forms.ModelForm):

    code = forms.CharField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)

    class Meta:
        model = Course
        fields = ('code', 'name', 'description')
