# General
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

# Opply
from .models import OrderProducts, Product


@receiver(post_save, sender=OrderProducts)
def order_products_changed(sender, instance, **kwargs):
    """ One method to deal with the decrement of quantity
        counter is to have a post save signal.

        There is a race condition here though, if two
        products are simultaneously bought, so we add
        a row lock mechanism via select_for_update, so
        subsequent queries have to wait on this completing.
    """

    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=instance.product.id)
        product.quantity_in_stock -= 1
        product.save()
