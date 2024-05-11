from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from .forms import MarketingSubscriptionForm


def index(request):
    """ A view to return the index page """

    form = MarketingSubscriptionForm()

    return render(request, 'home/index.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = MarketingSubscriptionForm(request.POST)
        if form.is_valid():
            instance = form.save()
            send_welcome_email(instance.email)
            messages.success(request, f'Thanks for subscribing! A welcome email and your discount code will be sent to {form.cleaned_data["email"]}.')
            return redirect('home')
        else:
            email = request.POST.get('email')
            messages.error(request, f'The email address {email} is already subscribed.')
            return redirect('home')
    else:
        form = MarketingSubscriptionForm()
    return render(request, 'home/index.html', {'form': form})


def send_welcome_email(subscriber_email):
    subject = render_to_string('home/subscription_welcome_email/subscription_welcome_email_subject.txt')
    message = render_to_string('home/subscription_welcome_email/subscription_welcome_email_body.text')
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [subscriber_email]
    send_mail(subject, message, sender_email, recipient_list)
