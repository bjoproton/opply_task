from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity_in_stock']


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

    products = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'user', 'datetime', 'products']
        read_only_fields = ('id', 'user', 'datetime')

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(
            user=self.context['user'], **validated_data)
        for product in products_data:
            order.products.add(product)
        return order
