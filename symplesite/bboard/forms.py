from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Bb, Rubric, Notes
from django import forms
from django.forms.widgets import DateInput
from captcha.fields import CaptchaField


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'kind')


class SomeSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search by product')
    captcha = CaptchaField(label='Enter text from the image',
                           error_messages={'invalid': 'Wrong text'})




class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=DateInput(attrs={'type': 'date'}))
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('comment',)





