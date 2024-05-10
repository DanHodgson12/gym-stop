from django import forms
from .models import MarketingSubscription


class MarketingSubscriptionForm(forms.ModelForm):
    class Meta:
        model = MarketingSubscription
        fields = ['email']
