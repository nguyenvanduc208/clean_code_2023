from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'created_at', 'updated_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        instance.user = validated_data.get('user', instance.user)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        order_items = instance.order_items.all()
        order_items = list(order_items)
        for order_item_data in order_items_data:
            if 'id' in order_item_data:
                order_item = next((item for item in order_items if item.id == order_item_data['id']), None)
                if order_item:
                    order_items.remove(order_item)
                    order_item.product = order_item_data.get('product', order_item.product)
                    order_item.quantity = order_item_data.get('quantity', order_item.quantity)
                    order_item.price = order_item_data.get('price', order_item.price)
                    order_item.save()
            else:
                OrderItem.objects.create(order=instance, **order_item_data)

        for order_item in order_items:
            order_item.delete()

        return instance
