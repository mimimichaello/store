from django.shortcuts import render, HttpResponsePermanentRedirect
from products.models import ProductCategory, Product, Basket
from users.models import User

def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)

def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists(): # Если наша корзина пустая или данного эл-та нет в ней
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else: # Если в корзине уже есть такой продукт
        basket = baskets.first()
        basket.quantity = basket.quantity + 1
        basket.save()

    return HttpResponsePermanentRedirect(request.META['HTTP_REFERER'])
    # Чтобы пользователь оставался на той странице на которой совершил действие

def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponsePermanentRedirect(request.META['HTTP_REFERER'])



