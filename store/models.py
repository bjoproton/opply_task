from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone


class Product(models.Model):
    """ Model to hold the product data.

        Had to make a choice here between storing a
        quantity_in_stock which was decremented on an
        action and storing a total stock available and
        counting the number of orders of that product
        dynamically. Could have, for example, used a
        property here to do this.

        With thousands of orders the property approach
        could be slow and wouldn't solve the race condition
        anyway.
    """
    name = models.CharField(max_length=64, null=False,
                            blank=False, default='', unique=True)
    price = models.DecimalField(null=False, blank=False, max_digits=20,
                                decimal_places=2,
                                validators=[MinValueValidator(0), ])
    quantity_in_stock = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    """ Model to hold the order information, for now this
        will only be id, user, datetime.

        The products, as there can be many per order will be
        held in another table.

        Note: Using get_user_model() here as it future proofs
              the possibility of using a custom user model.

        Note: We are protecting the user deletion here, so that
              a user can't be removed without explicitly deciding
              what do do with their linked orders.
    """
    user = models.ForeignKey(get_user_model(), null=False, blank=False,
                             on_delete=models.PROTECT, related_name='orders')
    datetime = models.DateTimeField(null=False, blank=False,
                                    default=timezone.now)


class OrderProducts(models.Model):
    """ Model to hold the product information linked to an
        order.

        Note: We are protecting the order deletion here, so that
              an order can't be removed without explicitly deciding
              what do do with their linked product order records.

        Note: We are protecting the product deletion here, so that
              a product can't be removed without explicitly deciding
              what do do with their linked product order records.
    """

    order = models.ForeignKey('Order', null=False, blank=False,
                              on_delete=models.PROTECT,
                              related_name='products')
    product = models.ForeignKey('Product', null=False, blank=False,
                                on_delete=models.PROTECT,
                                related_name='+')
