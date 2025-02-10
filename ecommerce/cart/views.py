import razorpay
from cart.models import Cart
from cart.models import Order_details, Payment
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product


# Create your views here.


@login_required
def addtocart(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            c.quantity += 1
            c.save()
            p.stock -= 1
            p.save()
    except:
        if (p.stock):
            c = Cart.objects.create(user=u, product=p, quantity=1)
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cartview')


@login_required
def cartview(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    total = 0
    for i in c:
        total += i.product.price * i.quantity
    context = {'cart': c, 't': total}
    return render(request, 'cart.html', context)


def cart_decrement(request, i):
    p = Product.objects.get(id=i)
    u = request.user

    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cartview')


def cart_delete(request, i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')


def order_form(request):
    if (request.method == 'POST'):
        a = request.POST['a']
        ph = request.POST['p']
        pin = request.POST['pin']
        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total += i.quantity * i.product.price
        total = int(total)
        # razorpay
        client = razorpay.Client(auth=('rzp_test_iUwTZ6Yz0paCFe', 'GLJIIvY2AX68lrrOtdNwHWGv'))
        response_payment = client.order.create(dict(amount=total * 100, currency='INR'))
        print(response_payment)
        order_id = response_payment['id']
        status = response_payment['status']
        if status == "created":
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()

            for i in c:
                o = Order_details.objects.create(product=i.product, user=i.user, phone=ph, address=a, pin=pin,
                                                 order_id=order_id, no_of_items=i.quantity)
                o.save()

            context = {'payment': response_payment, 'name': u.username}
            return render(request, 'payment.html', context)
    return render(request, 'orderform.html')


@csrf_exempt
def status(request, i):
    user = User.objects.get(username=i)
    login(request, user)
    response = request.POST
    print(response)
    param_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],

    }
    client = razorpay.Client(auth=('rzp_test_iUwTZ6Yz0paCFe','GLJIIvY2AX68lrrOtdNwHWGv'))
    try:
        status=client.utility.verify_payment_signature(param_dict)
        print(status)
        pay=Payment.objects.get(order_id=response['razorpay_order_id'])
        pay.paid=True
        pay.razorpay_payment_id=response['razorpay_order_id']
        pay.save()
        o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status = "Completed"
            i.save()
        c=Cart.objects.filter(user=user)
        c.delete()

    except:
        pass
    return render(request, 'status.html')


def orders(request):
    u=request.user
    p=Order_details.objects.filter(user=u,payment_status="Completed")
    print(p)
    context={'orders':p}
    return render(request,'orders.html',context)