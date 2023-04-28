from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'is_available': product.is_available,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        })
    return Response(data)


@api_view(['GET'])
def product_detail(request, product_id):
    query = f"SELECT * FROM products WHERE id = '{product_id}'"
    cursor = connection.cursor()
    cursor.execute(query)
    product_data = cursor.fetchall()
    return Response(product_data)



@api_view(['POST'])
def create_product(request):
    try:
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available')
        if not name or not description or not price or not is_available:
            return Response({'error': 'Missing required fields'})
        product = Product(name=name, description=description, price=price, is_available=is_available)
        product.save()
        data = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'is_available': product.is_available,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }
        return Response(data)
    except:
        return Response({'error': 'Missing required fields'})


@api_view(['PUT'])
def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')
    is_available = request.POST.get('is_available')
    if not name or not description or not price or not is_available:
        return Response({'error': 'Missing required fields'})
    product.name = name
    product.description = description
    product.price = price
    product.is_available = is_available
    product.save()
    data = {
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'is_available': product.is_available,
        'created_at': product.created_at,
        'updated_at': product.updated_at,
    }
    return Response(data)

@api_view(['DELETE'])
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return Response({'success': 'Product deleted successfully'})
