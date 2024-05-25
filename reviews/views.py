from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product


@login_required
def add_review(request, product_id):
    """ 
    A view to allow verified users to leave reviews
    on products they have previously purchased.
    """

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'reviews/add_review.html', context)


@login_required
def edit_review(request, review_id):
    """ 
    A view to allow verified users to edit a review
    they left on a product.
    """

    review = get_object_or_404(Review, id=review_id)

    # Ensure the user is the author of the review
    if review.user != request.user:
        messages.error(request, "You are not allowed to edit this review.")
        return redirect('product_detail', product_id=review.product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, f"Review for {review.product.name} updated successfully.")
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'product': review.product,
        'review': review
    }

    return render(request, 'reviews/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """ 
    A view to allow verified users to delete a review
    they left on a product.
    """

    review = get_object_or_404(Review, id=review_id)

    # Ensure the user is the author of the review
    if review.user != request.user:
        messages.error(request, "You are not allowed to delete this review.")
        return redirect('product_detail', product_id=review.product.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('product_detail', product_id=review.product.id)

    return redirect('product_detail', product_id=review.product.id)
