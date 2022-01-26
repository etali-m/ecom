import json
from .models import *

def cookieCart(request):
    #if the user is logged in for guest user
    #we start by getting the cart cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    #if the cart cookie does'nt exist we initialize it as an empty dictionnary
    except:
        cart = {} #cart is the cookie created who store the guest user products

    print('Cart: ', cart)
    items=[]
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
    cartItems = order['get_cart_items']

    #this loop is for getting the cart total for g
    for i in cart:
        #we use try block to prevent items in cart that may have been remove from the database
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            #variable below(item) is a dictionnary to get element of an orderitem
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total

            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order':order, 'items':items}


#this function is to get the cart data
def cartData(request):
    if request.user.is_authenticated: #we check if the user is authenticated to get all items of his order
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            #order is the retrieved or the created Order and created is a boolean
            #specifying wheter a new Order was created.
        items = order.orderitem_set.all()
            #We get all the order items who has order as a parent order
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order':order, 'items':items}


#this function is to proceed the guest user order
def guestOrder(request, data):
    print('User is not logged in..')

    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    
    #we will create a user or get it if he already existe
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    #we create the order
    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity'],
        )

    return  customer, order

