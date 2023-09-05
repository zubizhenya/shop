from django.forms import ModelForm
from .models import Bb
from django import forms
from django.forms.widgets import DateInput

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'kind')

class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=DateInput(attrs={'type': 'date'}))


