from django.urls import path

from .views import ProductViewSet, OrderViewSet

urlpatterns = [
    path('products', ProductViewSet.as_view({'get': 'list'})),
    path('products/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'})),
    path('orders', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<int:pk>', OrderViewSet.as_view({'get': 'retrieve'})),

]
