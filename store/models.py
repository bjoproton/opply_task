from django.db import models
from django.core.validators import MinValueValidator


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
