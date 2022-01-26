from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime


from .models import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):

    data = cartData(request)
    cartItems = data['cartItems'] 

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

    
def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
            

    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
     
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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


#this function is the process to save an order
def processOrder(request):
    transaction_id =  datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:#if the user is authenticated
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else: #if it is a guest user
       customer, order = guestOrder(request, data)

    #for any type of user who is checking out we have to confirm the total
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

    return JsonResponse('Payment complete..', safe=False) 