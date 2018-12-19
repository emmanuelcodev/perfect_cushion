from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.


def searchResult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        print('query is \n', query)
        products = Product.objects.all().filter(Q(name__contains = query) | Q(description__contains = query))
        print('products are \n', products)
    return render(request, 'search.html', {'query':query, 'products':products})
