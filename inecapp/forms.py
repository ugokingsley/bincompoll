from django import forms
from django.forms import ModelForm, Textarea

from .models import *


class AnnouncedPuResultsForm(forms.ModelForm):
	class Meta:
		model = AnnouncedPuResults
		fields = '__all__'
