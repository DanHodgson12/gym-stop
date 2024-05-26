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
    """ A view to return the index page. """

    form = MarketingSubscriptionForm()

    return render(request, 'home/index.html', {'form': form})


def privacy_policy(request):
    """ A view to return the Privacy Policy page. """

    return render(request, 'home/privacy_policy.html')


def terms_and_conditions(request):
    """ A view to return the Terms & Conditions page. """

    return render(request, 'home/terms_and_conditions.html')


def returns_policy(request):
    """ A view to return the Returns Policy page. """

    return render(request, 'home/returns_policy.html')


def page_not_found(request, exception):
    """ A view to return the 404 page. """

    return render(request, 'home/404.html', status=404)
