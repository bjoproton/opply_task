from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone


class Product(models.Model):
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
    products = models.ManyToManyField('Product', null=False, blank=False)
