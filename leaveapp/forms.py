from django import forms
from .models import *


class FormLeave(forms.ModelForm):
    from_date = forms.DateField(widget=forms.SelectDateWidget)
    to_date = forms.DateField(widget=forms.SelectDateWidget)
    station_add = forms.CharField(required=False )
    class Meta:
        model = Leave
        fields = ('leave_emp', 'leave_type', 'station_leave', 'station_add', 'from_date', 'to_date', 'acad_duty', 'administrative_duty')