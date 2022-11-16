from rest_framework import serializers
from exceptions import ProductOutOfStockException
from .models import Product, Order, OrderProducts


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity_in_stock']


class ProductsIdField(serializers.RelatedField):
    def to_representation(self, value):
        return value.product_id

    def to_internal_value(self, data):
        return Product.objects.get(id=data)


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer representing the API order object.

        Note: We're including the user here, even though
              the expectation is the user will be calling
              themselves. This will facilitate using the
              same serializer to deliver the data to, say, 
              a staff admin panel, at a later date, where
              they may wish to request many users orders.

        Note: This implementation of nested product
              serializer will return a structure like:
              {
                "id": 1,
                "user": 1,
                "datetime": "2022-11-16T18:57:05.944491Z",
                "products": [1, 2, 3]
             }
             With primary key ids for the products rather than
             full product data. This is to avoid rebuilding the 
             product data many times.  It's better to return a 
             list of product ids and do the lookups against some
             content data store on the front end, which would be 
             populated by calling the products endpoint e.g. at the
             beginning of a session and caching the data.

             Of course we don't have to use PKs here, we could use
             GUIDs, SKUs etc.
    """

    products = ProductsIdField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'user', 'datetime', 'products']
        read_only_fields = ('id', 'user', 'datetime')

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(
            user=self.context['user'], **validated_data)

        for product in products_data:
            if product.quantity_in_stock < 1:
                raise ProductOutOfStockException
            OrderProducts(order=order, product=product).save()
        return order
