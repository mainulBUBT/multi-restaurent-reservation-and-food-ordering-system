import string
import secrets
from decimal import Decimal
from sslcommerz_python.payment import SSLCSession
import socket
import requests
from .models import History, Order, Reservation, Restaurent
from Product_App.forms import ReserveForm
from App_Login.models import User, UserInfo
from Product_App.models import Product
from datetime import datetime
from urllib import response
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Sum
from cart.cart import Cart
from.helpers import render_to_pdf


# Create your views here.

def email_check(user):
    if not user.is_staff:
        return True


def index(request):
    restaurent = Restaurent.objects.all()
    return render(request, 'Product_App/index.html', {'values': restaurent})


@user_passes_test(email_check, login_url='/account/login/')
@login_required
def reservation(request, id):

    queryset = Restaurent.objects.filter(pk=id)
    restaurent = get_object_or_404(queryset, pk=id)
        
    # Getting specific restaurent seat capacity
    for seat in queryset:
        restaurent_seat = seat.total_seat

    cart = request.session.get('cart')
    if cart:
        for i in cart:
            restaurent_cart = cart[i]['restaurent_id']
            if restaurent_cart == restaurent.id:
                messages.warning(
                    request, "You have already booked this restaurent")
                return HttpResponseRedirect(reverse('Product_App:index'))
            elif Reservation.objects.filter(restaurents=restaurent, user=request.user):
                messages.warning(request, "Reservation process going on for this restaurent!")
                return HttpResponseRedirect(reverse('Product_App:index'))

    elif Reservation.objects.filter(restaurents=restaurent, user=request.user):
        print(Reservation.objects.filter(restaurents=restaurent, user=request.user))
        messages.warning(request, "Reservation process going on for this restaurent!")
        return HttpResponseRedirect(reverse('Product_App:index'))
    

   # Passes into the ReserveForm to make error
    form = ReserveForm(restaurent_seat=restaurent_seat)

    if request.method == 'POST':
        form = ReserveForm(restaurent_seat=restaurent_seat, data=request.POST)
        if form.is_valid():
            reserved = form.save(commit=False)
            reserved.user = request.user
            reserved.restaurents = restaurent
            reserved.save()
            messages.success(
                request, "Request for reservation successfull. Wait Please!")
            return HttpResponseRedirect(reverse('Product_App:index'))

    return render(request, 'Product_App/reservation.html', {'form': form, 'restaurent': queryset})


@user_passes_test(email_check, login_url='/account/login/')
def ur_reserve(request):
    table = Reservation.objects.filter(user=request.user)
    return render(request, 'Product_App/your_reserve.html', {'table': table})


def orders(request, tran_id, method, service_type, rest_id):

    cart = request.session.get('cart')

    # Getting Restaurent and User info
    for i in cart:
        restaurent_id = cart[i]['restaurent_id']
        user_id = cart[i]['userid']
        restaurent_name = Restaurent.objects.get(id=restaurent_id)
        user = User.objects.get(id=user_id)

        # Create Order Instance
    order = Order(
        image=restaurent_name.restaurent_pics,
        user=user,
        restaurents=restaurent_name,
        service_type=service_type,
        tran_id=tran_id,
        method=method,


    )
    order.save()

    # Track Order ID
    order_id = Order.objects.last()

    # Cart Item Insert into History
    for key, value in cart.items():

        val = value['restaurent_id']
        total = int(value['quantity'])*int(value['price'])
        product_id = value['product_id']
        products = Product.objects.get(id=product_id)

        # Corresponding restaurent get values and save it to History
        if int(val) == int(rest_id):
            history = History(
                order_id=order_id.id,
                restaurent_name=restaurent_name.name,
                restaurent_id=restaurent_name.id,
                product_name=products.name,
                product_img=products.image,
                product_id=product_id,
                price=value['price'],
                quantity=value['quantity'],
                user=request.user,
                service_type=service_type
            )
            history.save()

    request.session['cart'] = {}
    return redirect('Product_App:index')


def bill(request):
    if request.method == 'POST':
        store_id = "resta628cd6f96c3dc"
        API_KEY = "resta628cd6f96c3dc@ssl"
        mypayment = SSLCSession(
            sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_KEY)
        url = request.build_absolute_uri(reverse('Product_App:payments'))
        mypayment.set_urls(success_url=url, fail_url=url,
                           cancel_url=url, ipn_url=url)
        service_type = request.POST.get('service')
        total = request.POST.get('total')
        rest_id = request.POST.get('rest_id')
        mypayment.set_additional_values(value_a=service_type, value_b=rest_id)

        if service_type == 'waiter':
            amount = float(total) + 10
            mypayment.set_product_integration(total_amount=amount, currency='BDT', product_category='clothing',
                                              product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')
        else:
            amount = total
            mypayment.set_product_integration(total_amount=amount, currency='BDT', product_category='clothing',
                                              product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')

        mypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address',
                                    address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')

        mypayment.set_shipping_info(
            shipping_to='wstwfa', address='egagag', city='Dhaka', postcode='1209', country='Bangladesh')

        response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])


def test(request):
    pass


@csrf_exempt
def payments(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST

        status = payment_data['status']

        if status == 'VALID':
            tran_id = payment_data['tran_id']
            method = payment_data['card_issuer']
            service_type = payment_data['value_a']
            rest_id = payment_data['value_b']
            messages.success(request, "Payment Successfully")
            return HttpResponseRedirect(reverse('Product_App:orders', kwargs={'tran_id': tran_id, 'method': method, 'service_type': service_type, 'rest_id': rest_id},))
        print(payment_data)
    return HttpResponse("")


def menu_list(request, id):
    queryset = Restaurent.objects.filter(pk=id)
    restaurent = get_object_or_404(queryset, pk=id)
    table = Product.objects.filter(restaurents=restaurent)
    reserve_check = Reservation.objects.filter(restaurents=restaurent)

    for check in reserve_check:
        status = check.status
        user = check.user
        restaur = check.restaurents.id

    cart = request.session.get('cart')

    return render(request, 'Product_App/menus.html', {'table': table, 'status': status, 'user': user, 'cart': cart, 'restaur': restaur})


def check_cart(request, id):

    if request.method == 'POST':

        request.session['cart'] = {}
        messages.info(request, "Cart is empty. Add to cart!")
        return HttpResponseRedirect(reverse('Product_App:menus', kwargs={'id': id}))

    elif request.method == 'GET' or request.method == 'get':

        product = Product.objects.get(id=id)
        cart = request.session.get('cart')
        print(product.name)
        for i in cart:
            restaurent_id = cart[i]['restaurent_id']
        if cart == {}:
            return HttpResponseRedirect(reverse('Product_App:cart_add', kwargs={'id': id}))
        elif restaurent_id == product.restaurents.id:
            return HttpResponseRedirect(reverse('Product_App:cart_add', kwargs={'id': id}))
        elif restaurent_id != product.restaurents.id:
            print(restaurent_id)
            messages.warning(
                request, "You still have products from another restaurent. Shall we start over with a fresh CART?")
            return HttpResponseRedirect(reverse('Product_App:menus', kwargs={'id': product.restaurents.id}))


@login_required
def cart_add(request, id):

    cart = Cart(request)

    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id

    cart.add(product=product, restaurent=restaurent)
    messages.success(request, f'{product.name} added to the cart')
    return redirect("Product_App:menus", id=restaurent)


@login_required
def item_clear(request, id):

    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id
    cart.remove(product)

    return redirect("Product_App:cart_detail", id=restaurent)


@login_required
def item_increment(request, id):
    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id

    cart.add(product=product, restaurent=restaurent)
    return redirect("Product_App:cart_detail", id=restaurent)


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    queryset = Product.objects.filter(pk=id)
    product = get_object_or_404(queryset, pk=id)
    restaurent = product.restaurents.id
    cart.decrement(product=product, restaurent=restaurent)
    return redirect("Product_App:cart_detail", id=restaurent)


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("Product_App:cart_detail")


@login_required
def cart_detail(request, id):
    restaurent = Restaurent.objects.get(pk=id)
    cart = request.session.get('cart')

    # for i in cart:
    #     restaurent_id = cart[i]['restaurent_id']
    #     user_id = cart[i]['userid']

    if cart:
        for i in cart:
            restaurent_id = cart[i]['restaurent_id']
            prev_rest = Restaurent.objects.get(pk=restaurent_id)
        if restaurent.id == restaurent_id:
            return render(request, 'Product_App/cart/cart_detail.html', {'restaurent': restaurent, 'rest_id': restaurent.id})
        else:
            messages.info(request, f"{prev_rest} producrts have in your cart.")
            return HttpResponseRedirect(reverse('Product_App:ur_reserve'))

    else:
        messages.info(request, "Cart is empty")
        return redirect('Product_App:ur_reserve')


def generate_pdf(request, id):
    history = History.objects.filter(order_id=id)
    orders = Order.objects.get(id=id)
    count = history.count()
    service_type = orders.service_type
    # total = history.aggregate(Sum('price'))
    total = 0
    for i in history:
        total += int(i.price)*int(i.quantity)

    user_id = orders.user.id
    user_cell = UserInfo.objects.get(user=user_id)

    rec_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                     for i in range(20))

    data = {
        'history': history,
        'orders': orders,
        'count': count,
        'total': total,
        'service_type': service_type,
        'orders': orders,
        'date': datetime.now,
        'rec_id': rec_id,
        'cell': user_cell.cell,
    }
    pdf = render_to_pdf('invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def histories(request):
    history = History.objects.filter(user=request.user)

    orders = Order.objects.filter(user=request.user)

    
    return render(request, 'Product_App/history.html', {'histories':history, 'orders': orders})


def test(request, id):
    history = History.objects.filter(order_id=id)
    count = history.count()
    print(count)
    return render(request, 'Product_App/test.html')


def checkout(request):
    history = History.objects.filter(user=request.user)

    orders = Order.objects.filter(user=request.user)

    
    return render(request, 'Product_App/history.html', {'histories':history, 'orders': orders})
