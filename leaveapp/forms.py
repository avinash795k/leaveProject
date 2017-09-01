from django import forms
from .models import *


class FormLeave(forms.ModelForm):
    from_date = forms.DateField(widget=forms.SelectDateWidget)
    to_date = forms.DateField(widget=forms.SelectDateWidget)
    station_add = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'rows': 4}) )
    purpose = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = Leave
        fields = ('leave_type', 'station_leave', 'station_add', 'from_date', 'to_date', 'purpose', 'acad_duty', 'administrative_duty')