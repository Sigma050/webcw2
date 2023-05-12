import json
from paymentservice.models import User, Order, RefundOrder
from rest_framework.decorators import api_view
from datetime import datetime
import random
from django import forms
from django.http.response import JsonResponse


@api_view(['POST'])
def Register(request):
    data = json.loads(request.body)
    name = data.get('Name')
    email = data.get('Email')
    password = data.get('Password')
    user = User.objects.create(name=name, password=password, email=email, balance=0)
    if user:
        return JsonResponse({'AccountID': user.id, 'Name': name})
    return JsonResponse('Format wrong', status=400, safe=False)


@api_view(['POST'])
def Login(request):
    data = json.loads(request.body)
    id = data.get('ID')
    password = data.get('Password')
    user = User.objects.filter(id=id).first()
    if user and password == user.password:
        request.session['id'] = id
        return JsonResponse('success', status=200, safe=False)
    return JsonResponse('Format wrong', status=400, safe=False)


@api_view(['POST'])
def Orders(request):
    if request.session:
        data = json.loads(request.body)
        merchant_order_id = data.get('MerchantOrderId')
        price = data.get('Price')
        to_account = request.session['id']
        stamp = str(int(datetime.now().timestamp())) + str(random.randint(1000, 9999))
        order = Order.objects.create(merchant_order_id=merchant_order_id, order_time=datetime.now(),
                                     price=price, stamp=stamp, to_account=to_account)
        if order:
            return JsonResponse({'PaymentId': order.id, 'Stamp': order.stamp})
        return JsonResponse('Format wrong', status=400,safe= False)
    return JsonResponse('No login', status=400,safe = False)


@api_view(['POST'])
def Pay(request):
    if request.session:
        data = json.loads(request.body)
        payment_id = data.get('PaymentId')
        from_account = User.objects.get(id=request.session['id'])
        order = Order.objects.get(id=payment_id)
        if from_account.balance >= order.price:
            from_account.balance -= order.price
            order.from_account = from_account.id
            order.payment_time = datetime.now()
            to_account_id = order.to_account
            to_account = User.objects.get(id=to_account_id)
            to_account.balance += order.price
            order.save()
            from_account.save()
            to_account.save()
            return JsonResponse({'Stamp': order.stamp})
        return JsonResponse('Not enough money', status=400,safe= False)
    return JsonResponse('No login', status=400,safe= False)


@api_view(['POST'])
def Refund(request):
    if request.session:
        data = json.loads(request.body)
        payment_id = data.get('PaymentId')
        price = int(data.get('Price'))
        refund_orders = RefundOrder.objects.filter(payment_id=payment_id)
        price_all = price
        if refund_orders:
            for refund in refund_orders:
                price_all += refund.price
        if price_all <= int(Order.objects.get(id=payment_id).price):
            RefundOrder.objects.create(refund_time=datetime.now(),
                                       payment_id=payment_id, price=price)
            from_account = User.objects.get(id=request.session['id'])
            order = Order.objects.get(id=payment_id)
            to_account_id = order.to_account
            to_account = User.objects.get(id=to_account_id)
            from_account.balance += price
            to_account.balance -= price
            from_account.save()
            to_account.save()
            return JsonResponse('success', status=200,safe= False)
        return JsonResponse('Not enough money', status=400,safe= False)
    return JsonResponse('No login', status=400,safe= False)


@api_view(['GET'])
def Balance(request):
    if request.session:
        balance = User.objects.get(id=request.session['id']).balance
        return JsonResponse({'Balance': balance})
    return JsonResponse('No login', status=400,safe= False)


@api_view(['POST'])
def Deposit(request):
    if request.session:
        data = json.loads(request.body)
        price = data.get('Price')
        account = User.objects.get(id=request.session['id'])
        account.balance += int(price)
        account.save()
        return JsonResponse('success', status=200,safe= False)
    return JsonResponse('No login', status=400,safe= False)


