from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Returns a context dictionary containing the bag items, total cost,
    product count, delivery cost, amount needed to reach free delivery,
    free delivery threshold, and the grand total cost.
    """

    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        # Products that DO NOT have sizes
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        # Products that DO have sizes
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < Decimal(settings.FREE_DELIVERY_THRESHOLD):
        delivery_percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        delivery = total * delivery_percentage / Decimal('100.00')
        free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD) - total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    delivery = delivery.quantize(Decimal('0.00'))
    grand_total = (total + delivery).quantize(Decimal('0.00'))
    free_delivery_threshold = Decimal(
        settings.FREE_DELIVERY_THRESHOLD
    ).quantize(Decimal('0.00'))

    context = {
        'bag_items': bag_items,
        'total': total.quantize(Decimal('0.00')),
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta.quantize(Decimal('0.00')),
        'free_delivery_threshold': free_delivery_threshold,
        'grand_total': grand_total,
    }

    return context
