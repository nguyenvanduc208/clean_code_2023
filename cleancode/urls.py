"""
URL configuration for cleancode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import UserList, UserDetail, RegisterView, LoginView, LogoutView, ResetPasswordView
from products.views import product_list, create_product, update_product, product_detail
from orders.views import order_product, update_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path("products/", product_list, name="list product"),
    path("products/<int:pk>/", update_product, name="update product"),
    path("products/details/<int:pk>/", product_detail, name="detail product"),
    path("products/", create_product, name="create product"),
    path("orders/", order_product, name="create orders"),
    path('order/<int:pk>/update/', update_order, name="update oder view"),
]
