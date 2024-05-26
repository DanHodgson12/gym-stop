from .forms import MarketingSubscriptionForm


def subscribe_form(request):
    return {
        'subscribe_form': MarketingSubscriptionForm()
    }
