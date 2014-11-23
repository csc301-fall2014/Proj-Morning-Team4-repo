from school.models import SchoolProfile, Course
from django import forms
from main.models import Student
from django.contrib.auth.models import User


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('school',)



class CourseForm(forms.ModelForm):
	# to create a course?

    class Meta:
        model = Course
        fields = ('code', 'name', 'description',)
        widgets = {
        	'code': forms.TextInput(attrs={'class': 'form-control'}),
        	'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }	
	
	
	
class StudentAdminForm(forms.ModelForm):
	# to create a student admin

    class Meta:
	model = Course
	fields = ('student_admins',)	
	student_admins = student_admins = forms.ModelMultipleChoiceField( queryset=Student.objects.all(), required=False)