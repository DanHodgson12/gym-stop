from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
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
    User = get_user_model()

    if request.method == 'POST':
        form = MarketingSubscriptionForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                profile = user.userprofile
                if profile.is_subscribed_to_newsletter:
                    messages.error(
                        request,
                        f'The email address {email} is already subscribed '
                        'to our mailing list, and is associated with an '
                        'existing account.'
                    )
                    return redirect('home')
                else:
                    profile.is_subscribed_to_newsletter = True
                    profile.save()
            else:
                form.save()
            subscriber_email = request.POST.get('email')
            send_welcome_email(subscriber_email)
            messages.success(
                request,
                f'Thanks for subscribing to our mailing list! A welcome '
                f'email has been sent to {subscriber_email}.'
            )
            return redirect('home')
        else:
            email = request.POST.get('email')
            messages.error(
                request,
                f'The email address {email} is already '
                'subscribed to our mailing list.'
            )
            return redirect('home')
    else:
        form = MarketingSubscriptionForm()
    return render(request, 'home/index.html', {'form': form})


def unsubscribe(request):
    User = get_user_model()

    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber = (
                MarketingSubscription.objects
                .filter(email=email)
                .first()
            )
            user = User.objects.filter(email=email).first()
            if subscriber or user:
                if subscriber:
                    subscriber.delete()
                if user:
                    profile = user.userprofile
                    if not profile.is_subscribed_to_newsletter:
                        messages.error(
                            request,
                            f'The email address {email} is '
                            'not on our mailing list.'
                        )
                        return redirect('home')
                    else:
                        profile.is_subscribed_to_newsletter = False
                        profile.save()
                messages.success(
                    request,
                    f'The email address {email} has been successfully '
                    'unsubscribed from our mailing list.'
                )
                return redirect('home')
            else:
                messages.error(
                    request,
                    f'The email address {email} is not on our mailing list.'
                )
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

    subject = render_to_string(
        'home/subscription_email/subscription_email_subject.txt'
    )
    message_text = render_to_string(
        'home/subscription_email/subscription_email_body.txt',
        {'unsubscribe_url': unsubscribe_url}
    )
    message_html = render_to_string(
        'home/subscription_email/subscription_email_body.html',
        {'unsubscribe_url': unsubscribe_url}
    )

    email = EmailMultiAlternatives(
        subject, strip_tags(message_text), sender_email, receiver_email
    )
    email.attach_alternative(message_html, "text/html")

    try:
        email.send()
        return True  # or return some success message if needed
    except Exception as e:
        print(f"Failed to send welcome email to {subscriber_email}: {str(e)}")
        return False  # or return some failure message
