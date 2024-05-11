from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
import os
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import MarketingSubscription
from .forms import MarketingSubscriptionForm
from .forms import UnsubscribeForm


def index(request):
    """ A view to return the index page """

    form = MarketingSubscriptionForm()

    return render(request, 'home/index.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = MarketingSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            subscriber_email = request.POST.get('email')
            send_welcome_email(subscriber_email)
            messages.success(request, f'Thanks for subscribing! A welcome email has been sent to {subscriber_email}.')
            return redirect('home')
        else:
            email = request.POST.get('email')
            messages.error(request, f'The email address {email} is already subscribed.')
            return redirect('home')
    else:
        form = MarketingSubscriptionForm()
    return render(request, 'home/index.html', {'form': form})


def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber = MarketingSubscription.objects.filter(email=email).first()
            if subscriber:
                subscriber.delete()
                messages.success(request, 'You have been successfully unsubscribed.')
                return redirect('home')
            else:
                messages.error(request, 'No subscriber found with this email address.')
                return redirect('unsubscribe')
    else:
        form = UnsubscribeForm()
    return render(request, 'home/unsubscribe.html', {'form': form})


def send_welcome_email(subscriber_email):
    sender_email = settings.DEFAULT_FROM_EMAIL
    receiver_email = [subscriber_email,]

    if 'DEVELOPMENT' in os.environ and os.environ['DEVELOPMENT'] == 'True':
        base_url = 'http://localhost:8000'
    else:
        base_url = 'https://danh12-gym-stop-6494ee93884f.herokuapp.com'

    unsubscribe_url = f'{base_url}/unsubscribe/'

    subject = render_to_string('home/subscription_welcome_email/subscription_welcome_email_subject.txt')
    message_text = render_to_string('home/subscription_welcome_email/subscription_welcome_email_body.text', {'unsubscribe_url': unsubscribe_url})
    message_html = render_to_string('home/subscription_welcome_email/subscription_welcome_email_body.html', {'unsubscribe_url': unsubscribe_url})

    email = EmailMultiAlternatives(subject, strip_tags(message_text), sender_email, receiver_email)
    email.attach_alternative(message_html, "text/html")
    
    try:
        email.send()
        return True  # or return some success message if needed
    except Exception as e:
        print(f"Failed to send welcome email to {subscriber_email}: {str(e)}")
        return False  # or return some failure message
