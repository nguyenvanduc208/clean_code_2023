from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity", "price"]

    def get_price(self, obj):
        return obj.product.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "ordered_items", "total_price"]

    def get_ordered_items(self, obj):
        ordered_items = OrderItem.objects.filter(order__id=obj.id)
        serializer = OrderItemSerializer(ordered_items, many=True)
        return serializer.data

    def get_total_price(self, obj):
        total_price = 0
        ordered_items = self.get_ordered_items(obj)
        for item in ordered_items:
            total_price += float(item["price"])
        return total_price
