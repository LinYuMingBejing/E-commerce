from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from api.models import Product, Order


def inventory_check(func):

    @transaction.atomic
    def wrapper(request, *args, **kwargs):
        count = request.POST.get('quantity', None)
        product_id = request.POST.get('product_id', None)
        
        save_id = transaction.savepoint()

        try:
            product = Product.objects.select_for_update().get(id=product_id)
        except:
            transaction.savepoint_rollback(save_id)
            messages.error(request, '商品不存在')
            return redirect('index')

        if int(count) > product.stock_pcs:
            transaction.savepoint_rollback(save_id)
            messages.error(request, '貨源不足')
            return redirect('index')
        
        product.sales += int(count)
        product.stock_pcs -= int(count)
        product.save()
        return func(request, *args, **kwargs)
    return wrapper


def delete_order(func):

    @transaction.atomic
    def wrapper(request, *args, **kwargs):
        order_id = request.POST.get('order_id', None)

        save_id = transaction.savepoint()

        try:
            order = Order.objects.select_for_update().get(id=order_id)
        except:
            transaction.savepoint_rollback(save_id)
            messages.error(request, '訂單不存在')
            return redirect('index')
        
        try:
            product = Product.objects.select_for_update().get(id=order.product_id)
        except:
            transaction.savepoint_rollback(save_id)
            messages.error(request, '商品不存在')
            return redirect('index')

        if product.stock_pcs == 0:
            messages.info(request, '商品到貨')

        product.sales -= int(order.qty)
        product.stock_pcs += order.qty
        product.save()
        return func(request, *args, **kwargs)
    
    return wrapper


def authentication(func):
    def wrapper(request, *args, **kwargs):
        is_vip     = request.POST.get('is_vip', None)
        product_id = request.POST.get('product_id', None)

        product = get_object_or_404(Product, id=product_id)
        if product.is_vip and not is_vip:
            messages.error(request, '權限不足')
            return redirect('index')
        else:
            return func(request, *args, **kwargs)

    return wrapper
