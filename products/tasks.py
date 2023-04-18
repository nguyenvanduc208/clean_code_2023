from decimal import Decimal
from products.models import Product


def update_product_prices(tax_rate):
    products = Product.objects.all()
    for product in products:
        if product.tax_rate:
            product.price = product.cost_price * (Decimal(1) + tax_rate)
            product.save()
