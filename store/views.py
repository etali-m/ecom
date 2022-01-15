from django.shortcuts import render
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

    
def cart(request):

    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
            #We get all the order items who has order as a parent order
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order':order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
            #We get all the order items who has order as a parent order
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order':order}
    return render(request, 'store/checkout.html', context)