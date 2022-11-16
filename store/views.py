# General
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_authtoken.auth import AuthTokenAuthentication

# Opply
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (AuthTokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (AuthTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-datetime')

    def get_serializer_context(self):
        return {'user': self.request.user}
