from django.urls import path

from products import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list product"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="update product"),
]
