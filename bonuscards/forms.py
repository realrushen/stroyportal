from django import forms
from .models import BonusCard


class BonusCardForm(forms.ModelForm):
    class Meta:
        model = BonusCard
        fields = (
            'series', 
            'number', 
            'release_date', 
            'activity_expires_date',
            'use_date',
            'amount',
            'activity_status'
        )
