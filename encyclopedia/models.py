from django.db import models
from django import forms

# Create your models here.
class PageForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea)