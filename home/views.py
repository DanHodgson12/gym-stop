from django.shortcuts import render


def index(request):
    """
    A view to return the index page.
    """

    return render(request, 'home/index.html')


def privacy_policy(request):
    """
    A view to return the Privacy Policy page.
    """

    return render(request, 'home/privacy_policy.html')


def terms_and_conditions(request):
    """
    A view to return the Terms & Conditions page.
    """

    return render(request, 'home/terms_and_conditions.html')


def returns_policy(request):
    """
    A view to return the Returns Policy page.
    """

    return render(request, 'home/returns_policy.html')


def page_not_found(request, exception):
    """
    A view to return the 404 page.
    """

    return render(request, 'home/404.html', status=404)
