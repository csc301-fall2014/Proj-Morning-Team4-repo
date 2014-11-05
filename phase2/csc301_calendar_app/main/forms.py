from main.models import Student
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
        	'username': forms.TextInput(attrs={'class': 'form-control'}),
        	'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
    	model = Student
    	fields = ('nickname', ) # , 'schools' )
        widgets = {
        	'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
