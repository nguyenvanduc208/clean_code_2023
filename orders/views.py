from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_product(request, pk):
    user = request.user
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__pk=product.pk).exists():
                order_item = OrderItem.objects.filter(product=product, user=user, ordered=False)[0]
                order_item.quantity += 1
                order_item.save()
                return Response(status=status.HTTP_200_OK)
            else:
                order_item = OrderItem.objects.create(product=product, user=user)
                order.products.add(order_item)
                return Response(status=status.HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=user, ordered_date=ordered_date)
            order_item = OrderItem.objects.create(product=product, user=user, ordered=False)
            order.products.add(order_item)
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    order_items = OrderItem.objects.filter(order=order)
    serializer = OrderItemSerializer(order_items, many=True)

    order_serializer = OrderSerializer(order)
    order_data = order_serializer.data

    order_data['order_items'] = serializer.data

    return Response(order_data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
