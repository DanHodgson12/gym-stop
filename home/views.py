from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import MarketingSubscriptionForm


def index(request):
    """ A view to return the index page """

    form = MarketingSubscriptionForm()

    return render(request, 'home/index.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        form = MarketingSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Thanks for subscribing! A welcome email and your discount code will be sent to {form.cleaned_data["email"]}.')
            return redirect('home')
        else:
            email = request.POST.get('email')
            messages.error(request, f'The email address {email} is already subscribed.')
            return redirect('home')
    else:
        form = MarketingSubscriptionForm()
    return render(request, 'home/index.html', {'form': form})
