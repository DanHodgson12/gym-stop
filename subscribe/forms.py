from django import forms
from .models import MarketingSubscription


class MarketingSubscriptionForm(forms.ModelForm):
    """
    Form for subscribing to marketing emails.
    """

    class Meta:
        model = MarketingSubscription
        fields = ['email']


class UnsubscribeForm(forms.Form):
    """
    Form for unsubscribing from marketing emails.
    """

    email = forms.EmailField(label='Email')
