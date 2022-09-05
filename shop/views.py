from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from .models import Category, Product, Order, OrderProduct
from .utils import Utils
from datetime import datetime


def home(request):
    context = {
        'base': Utils.getBaseContect(request),
        'categories': Category.objects.filter(featured=True),
        'products': Product.objects.filter(featured=True)
    }

    return render(request, 'home.html', context)


def categories(request):
    categories = Category.objects.filter()
    context = {
        'base': Utils.getBaseContect(request),
        'categories': categories
    }

    return render(request, 'categories.html', context)


def category_detail(request, **kwargs):
    category = Category.objects.filter(slug=kwargs['slug']).first()
    products = Product.objects.filter(category=category.id) if category != None else None
    context = {
        'base': Utils.getBaseContect(request),
        'category': category,
        'products': products
    }

    return render(request, 'category_detail.html', context)


def product_detail(request, **kwargs):
    context = {
        'base': Utils.getBaseContect(request),
        'product': Product.objects.filter(slug=kwargs['slug']).first()
    }

    return render(request, 'product_detail.html', context)


def cart(request):
    cart = Order.objects.filter(session_key=request.session.session_key, finalized=False).first()
    products = OrderProduct.objects.filter(order=cart)
    total = 0
    for prod in products:
        total += prod.price * prod.qty
    context = {
        'base': Utils.getBaseContect(request),
        'products': products,
        'total': total
    }

    return render(request, 'cart.html', context)


def about(request):
    context = {
        'base': Utils.getBaseContect(request)
    }

    return render(request, 'about.html', context)


def cart_submit(request):

    if request.POST['action'] == 'submit':
        order = Order.objects.get(session_key=request.session.session_key, finalized=False)
        order.customer_name = request.POST['name']
        order.customer_address = request.POST['address']
        order.customer_phone = request.POST['phone']
        order.finalized = True
        order.date = datetime.now()

        order.content = ''
        order.price = 0
        orderedProducts = OrderProduct.objects.filter(order=order)
        for prod in orderedProducts:
            order.content += prod.product.name + ' [' + prod.product.slug + '] ' + str(prod.price) + 'руб.' + ' x' + str(prod.qty) + '\n'
            order.price += prod.price * prod.qty

        order.save()
        return HttpResponseRedirect('/cart/thanks')


def cart_thanks(request):
    context = {
        'base': Utils.getBaseContect(request)
    }

    return render(request, 'cart_thanks.html', context)



def cart_action(request):

    if request.GET['action'] == 'add' and request.GET['id'] != None:
        product = Product.objects.get(id=request.GET['id'])
        order, created = Order.objects.get_or_create(session_key=request.session.session_key, finalized=False)
        orderProduct, created = OrderProduct.objects.get_or_create(product=product, order=order)
        orderProduct.qty = 1 if created else orderProduct.qty + 1
        orderProduct.price = product.price
        orderProduct.save()

    if request.GET['action'] == 'delete' and request.GET['id'] != None:
        product = Product.objects.get(id=request.GET['id'])
        order = Order.objects.get(session_key=request.session.session_key, finalized=False)
        orderProduct = OrderProduct.objects.get(product=product, order=order)
        orderProduct.qty = orderProduct.qty - 1
        if orderProduct.qty <= 0:
            orderProduct.delete()
        else:
            orderProduct.save()

    order = Order.objects.get(session_key=request.session.session_key, finalized=False)
    order.content = ''
    order.price = 0
    orderedProducts = OrderProduct.objects.filter(order=order)
    for prod in orderedProducts:
        order.content += prod.product.name + ' [' + prod.product.slug + '] ' + str(prod.price) + 'руб.' + ' x' + str(prod.qty) + '\n'
        order.price += prod.price * prod.qty
    order.date = datetime.now()
    order.save()
        
    return HttpResponse(OrderProduct.objects.filter(order=order).aggregate(Sum('qty'))['qty__sum'])


