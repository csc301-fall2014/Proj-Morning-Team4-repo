from school.models import SchoolProfile
from django import forms


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = ('school_name',)
