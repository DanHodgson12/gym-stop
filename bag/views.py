from django.shortcuts import render, redirect, reverse, HttpResponse


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # If the product DOES have a size
    if size:
        # If same product is already in bag, do this
        if item_id in list(bag.keys()):
            # If same product with same size is already in bag, update quantity for that product in 'items_by_size' dictionary
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            # If product with different size is being added to bag, add new 'size' and 'quantity' to 'items_by_size' dictionary
            else:
                bag[item_id]['items_by_size'][size] = quantity
        # If same product is NOT already in bag, add it with quantity set to dictionary called 'items_by_size', with inner dictionary of 'size' and 'quantity'
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # If the product DOES NOT have a size
    else:
        # If same product is already in bag, update quantity for that product
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        # If same product is NOT already in bag, update quantity for that product
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
