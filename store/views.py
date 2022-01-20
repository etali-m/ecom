from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime


from .models import *

# Create your views here.
def store(request):

    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

    
def cart(request):

    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
            #We get all the order items who has order as a parent order
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
            #We get all the order items who has order as a parent order
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body) #we load the json data sended in update_item url in the cart.js file
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:', productId)

    customer = request.user.customer #we are getting the logged in customer
    product = Product.objects.get(id=productId) 

    #now we want to get order of the customer or create it if it doesn't exist
    order, created = Order.objects.get_or_create(customer=customer, complete=False)  

    #Now we create an OrderItem for the order we have created
    #we get_or_create because we need to change the value of the orderItem if it
    #already exist we will add or substract the quantity of product
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity ==0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False) 


#this function is the process to save order
def processOrder(request):
    transaction_id =  datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total): 
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )

    else:
        print('User is not logged in..')
    return JsonResponse('Payment complete..', safe=False) 