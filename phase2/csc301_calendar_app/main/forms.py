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

class UserTypeForm(forms.Form):
    CHOICES=(('0', 'Instructor',), ('1', 'Student',))
    user_type = forms.ChoiceField(
            widget=forms.RadioSelect(
                attrs={},
            ), 
            choices=CHOICES, 
            required=True
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
    	model = UserProfile
    	fields = ('nickname', ) # , 'schools' )
        widgets = {
        	'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }
