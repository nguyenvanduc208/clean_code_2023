from django.urls import path

from orders import views

urlpatterns = [
    path("", views.OrderProduct.as_view(), name="list product"),
    path("<int:pk>/", views.OrderDetail.as_view(), name="update oder view"),
    # path("details/<int:pk>/", views.product_detail, name="detail product"),
    # path("products/", create_product, name="create product"),
]
