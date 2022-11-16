# General
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_authtoken.auth import AuthTokenAuthentication

# Opply
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (AuthTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
