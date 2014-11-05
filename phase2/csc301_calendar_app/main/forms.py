from main.models import UserProfile
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

class UserProfileForm(forms.ModelForm):
    class Meta:
    	model = UserProfile
    	fields = ('nickname', ) # , 'schools' )
        widgets = {
        	'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
