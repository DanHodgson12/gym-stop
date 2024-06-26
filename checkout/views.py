from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents
import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    A view to cache user's checkout data.
    """

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    A view to render the checkout page and process user's order.
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # If user submits the checkout form, do this...

        # Retrieve bag data
        bag = request.session.get('bag', {})

        # Retrieve form data
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        # Create instance of an order form using the above checkout form data
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # If order_form IS valid...

            # Save order_form
            order = order_form.save(commit=False)

            # Get Payment Intent ID from client secret input in checkout form
            pid = request.POST.get('client_secret').split('_secret')[0]

            # Set 'stripe_pid' & 'original_bag' fields on order model
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            # Iterate through bag items
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)

                    # If item DOES NOT have size, create line item for each
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    # If item DOES have size, create line item for each size
                    else:
                        for s, q in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=q,
                                product_size=s,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    # If product does not exist, delete order and redirect user
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our "
                        "database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Check if customer wants to save their checkout info
            request.session['save_info'] = 'save-info' in request.POST

            # ORDER SUCCESSFUL!!! Perform 'checkout_success' function
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            # If order_form IS NOT valid...

            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        # When user first hits checkout page, do this...

        # Retrieve bag data
        bag = request.session.get('bag', {})

        # If no bag, redirect customer back to products page
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill form with any info user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if 'intent' in locals() else '',
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    A view to render the checkout success page
    and handle successful orders.
    """

    # Check user wanted to save their info - used to add to user profile
    save_info = request.session.get('save_info')

    # Grab the order data for this particular order
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_country': order.country,
                'default_postcode': order.postcode,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    # Let the user know their order was successful by displaying message
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Delete bag data as no longer needed
    if 'bag' in request.session:
        del request.session['bag']

    # Render template and send through order in context
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
