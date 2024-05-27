from .forms import MarketingSubscriptionForm


def subscribe_form(request):
    """
    Context processor to add the marketing subscription form to the context.
    """

    return {
        'subscribe_form': MarketingSubscriptionForm()
    }
