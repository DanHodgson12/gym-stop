from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
import os
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import MarketingSubscription
from .forms import MarketingSubscriptionForm
from .forms import UnsubscribeForm


def subscribe(request):
    """
    A view to handle user subscription to the mailing list.

    If the request method is POST, it processes the subscription form.
    If the subscription is successful, it sends a welcome email.
    """

    User = get_user_model()

    if request.method == 'POST':
        subscribe_form = MarketingSubscriptionForm(request.POST)
        if subscribe_form.is_valid():
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
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    profile.is_subscribed_to_newsletter = True
                    profile.save()
            else:
                subscribe_form.save()
            subscriber_email = request.POST.get('email')

            try:
                send_welcome_email(subscriber_email)
                messages.success(
                    request,
                    f'Thanks for subscribing to our mailing list! A welcome '
                    f'email has been sent to {subscriber_email}.'
                )
            except Exception as e:
                messages.error(
                    request,
                    f"Failed to send welcome email to {subscriber_email}: {str(e)}"
                )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            email = request.POST.get('email')
            messages.error(
                request,
                f'The email address {email} is already '
                'subscribed to our mailing list.'
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        subscribe_form = MarketingSubscriptionForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def unsubscribe(request):
    """
    A view to render the unsubscribe page and handle unsubscriptions.

    Renders the unsubscribe page with a form to submit an email address.
    If the form is submitted and valid, unsubscribes the user from the mailing list.
    """

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
    return render(request, 'subscribe/unsubscribe.html', {'form': form})


def send_welcome_email(subscriber_email):
    """
    A function to send a welcome email to a new subscriber.

    Sends a welcome email to the provided email address
    with a link to unsubscribe from the mailing list.
    """

    sender_email = settings.DEFAULT_FROM_EMAIL
    receiver_email = [subscriber_email,]

    if 'DEVELOPMENT' in os.environ and os.environ['DEVELOPMENT'] == 'True':
        base_url = os.environ.get('DEVELOPMENT_URL')
    else:
        base_url = 'https://danh12-gym-stop-6494ee93884f.herokuapp.com'

    unsubscribe_url = f'{base_url}/unsubscribe/'

    subject = render_to_string(
        'subscribe/subscription_email/subscription_email_subject.txt'
    )
    message_text = render_to_string(
        'subscribe/subscription_email/subscription_email_body.txt',
        {'unsubscribe_url': unsubscribe_url}
    )
    message_html = render_to_string(
        'subscribe/subscription_email/subscription_email_body.html',
        {'unsubscribe_url': unsubscribe_url}
    )

    email = EmailMultiAlternatives(
        subject, strip_tags(message_text), sender_email, receiver_email
    )
    email.attach_alternative(message_html, "text/html")

    email.send()
