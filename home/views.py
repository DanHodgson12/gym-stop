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
            # Optionally, generate and send a discount code to the subscriber
            messages.success(request, f'Thanks for subscribing! A welcome email and your discount code will be sent to {form.cleaned_data["email"]}.')
            return redirect('home')
    else:
        form = MarketingSubscriptionForm()
        messages.error(request, 'An error occurred when submitting your form. Please try again.')
    return render(request, 'home/index.html', {'form': form})
