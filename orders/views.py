from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from orders.models import Product, Order, OrderItem
from orders.serializers import OrderSerializer


class OrderProduct(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product = Product.objects.get(id=request.data["product_id"])

        order_qs = Order.objects.filter(user=user, complete=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(id=product.pk).exists():
                order_item = OrderItem.objects.filter(product=product, order=order)[0]
                order_item.quantity += 1
                order_item.save()
                return Response(status=status.HTTP_200_OK)
            else:
                order_item = OrderItem.objects.create(product=product, order=order)
                return Response(status=status.HTTP_200_OK)
        else:
            order = Order.objects.create(user=user)
            order_item = OrderItem.objects.create(product=product, order=order)
            return Response(status=status.HTTP_200_OK)
        

class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Order, id=pk)

    def get(self, request, pk):
        order = self.get_object(pk)

        if order.user != request.user:
            return Response({"error": "You cannot view other's orders"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        order = self.get_object(pk)

        if order.user != request.user:
            return Response({"error": "You cannot view other's orders"}, status=status.HTTP_400_BAD_REQUEST)
        
        items = request.data.get("ordered_items")
        for item in items:
            product_id = item.get("product")
            inv_item = OrderItem.objects.get(product_id=product_id, order_id=order.id)
            inv_item.quantity = item.get("quantity")
            inv_item.save()
        
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
