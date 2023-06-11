import json

from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from customers.models import Customers
from rest_framework.response import Response
from .models import Carts, CartItems
from products.models import Products
from .serializers import CartSerializer


class CartsView(APIView):

    # 查看购物车信息
    def get(self, request):
        cart_id = request.query_params.get('id')

        cart = cache.get(f'cart:{cart_id}')
        if cart is not None:
            cart_data = CartSerializer(cart).data
            return Response({
                'code': '200',
                'data': cart_data
            })

        cart = Carts.objects.filter(id=cart_id).first()
        if not cart:
            return Response({
                'code': '404',
                'msg': 'Cart not found'
            })
        cart_data = CartSerializer(cart).data
        cache.set(f'cart:{cart.id}', cart, timeout=60 * 10)
        return Response({
            'code': '200',
            'data': cart_data
        })

    # 创建一个购物车
    def post(self, request):
        cart_data = request.data
        # 先判断是否存在指定的customer, 并且判断用户是否已经创建了购物车
        customer = Customers.objects.filter(bc_id=cart_data['customer_id']).first()
        cart = Carts.objects.filter(customer_id=cart_data['customer_id']).first()

        if not customer:
            return Response({
                'code': 400,
                'msg': 'Customer not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif cart:
            return Response({
                'code': 400,
                'msg': 'Cart already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart = Carts.objects.create(
            customer=customer
        )
        serial_cart = CartSerializer(cart).data
        return Response({
            'code': 200,
            'msg': 'Cart created successfully',
            'data': serial_cart
        })


class CartItemsView(APIView):

    # 将商品加入购物车
    def post(self, request, cart_id=None):
        item_data = request.data.copy()
        prod_id = item_data['product_id']
        product_query = Products.objects.filter(bc_pro_id=prod_id)
        cart = Carts.objects.filter(id=cart_id).first()

        if not product_query.exists():
            return Response({
                'code': 400,
                'message': 'Product not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItems.objects.filter(product_id=prod_id, cart_id=cart_id).first()
        # 如果要添加的商品,则只添加数量就行
        if cart_item:
            cart_item.quantity += item_data['quantity']
            # 更新item中的信息
            cart_item.save()
            # 购物车中的信息
            cart.update_total()

            return Response({
                'code': 200,
                'msg': 'Add items to cart successfully'
            })
        else:
            CartItems.objects.create(
                quantity=item_data['quantity'],
                cart_id=cart_id,
                product_id=prod_id,
                price=product_query.first().price
            )

            cart.update_total()

            return Response({
                'code': 200,
                'msg': 'Add items to cart successfully'
            })

    # 更新购物车商品条目信息
    def put(self, request, cart_id=None):
        quantity = request.data['quantity']
        prod_id = request.data['product_id']
        increase_or_reset = request.data['increase_or_reset']

        item = CartItems.objects.filter(cart_id=cart_id, product_id=prod_id).first()
        cart = Carts.objects.filter(id=cart_id).first()

        if not item:
            return Response({
                'code': 400,
                'msg': 'There is no corresponding product in the shopping cart'
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            if increase_or_reset == 0:
                # 重置
                item.quantity += quantity
            elif increase_or_reset == 1:
                # 增加
                item.quantity = quantity
            else:
                # 减少
                if quantity > item.quantity:
                    return Response({
                        'code': 400,
                        'msg': 'Decrease Quantity Exceeding Current Item Quantity'
                    }, status=status.HTTP_400_BAD_REQUEST)
                item.quantity -= quantity
            if item.quantity == 0:
                item.delete()
            else:
                item.save()
            cart.update_total()

            return Response({
                'code': 200,
                'msg': 'Update successful'
            })

    # 删除购物车条目
    def delete(self, request, cart_id=None):
        cart = Carts.objects.filter(id=cart_id).first()
        prod_id = request.data['product_id']
        item = CartItems.objects.filter(cart_id=cart_id, product_id=prod_id)

        if not item.exists():
            return Response({
                'code': 400,
                'msg': 'There is no corresponding product in the shopping cart'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            item.delete()
            cart.update_total()

            return Response({
                'code': 200,
                'msg': 'Delete cart item successfully'
            })
