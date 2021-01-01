from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator

from api.models import Product, Order, Shop
from api.decorator import inventory_check, authentication, delete_order


# Create your views here.
class IndexView(View):
    """首頁"""
    def get(self, request):
        products = Product.objects.all()
        orders = Order.objects.filter(is_delete=False)
        return render(
            request, 
            'index.html', 
            {
                'products': products, 'orders': orders
            }
        )


class OrderCommitView(View):
    """訂單查詢"""

    @method_decorator(inventory_check)
    @method_decorator(authentication)
    @transaction.atomic
    def post(self, request):
        count = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        customer_id = request.POST.get('customer_id')

        if not all([product_id, count, customer_id]):
            return JsonResponse({'status': False, 'msg': '參數不完整'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': False, 'msg': '商品不存在'})
        
        try:
            shop = Shop.objects.get(id=product.shop_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': False, 'msg': '商品不存在'})

        Order.objects.create(product= product, 
                            customer_id=customer_id, 
                            qty = int(count),
                            price = int(count) * product.price, 
                            shop = shop)
        return redirect('index')


class OrderDeleteView(View):
    """訂單刪除"""

    @method_decorator(delete_order)
    def post(self, request):
        order_id = request.POST.get('order_id', None)
        order = Order.objects.get(id=order_id)
        order.is_delete = True
        order.save()
        return redirect('index')


class OrderCheckView(View):
    def post(self, request):
        products = Product.objects.order_by('-sales')[:3]
        hot_products = [product.id for product in products]
        messages.info(request, hot_products)
        return redirect('index')