from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
import os
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from subscribe.models import MarketingSubscription
from subscribe.forms import MarketingSubscriptionForm
from subscribe.forms import UnsubscribeForm


def index(request):
    """ A view to return the index page """

    form = MarketingSubscriptionForm()

    return render(request, 'home/index.html', {'form': form})
