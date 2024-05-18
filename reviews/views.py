from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.all()

    context = {
        'reviews': reviews
    }

    return render(request, 'reviews/review_list.html', context)


def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user if request.user.is_authenticated else None
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'reviews/add_review.html', context)
