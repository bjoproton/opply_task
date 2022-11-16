from store.models import Product
from django.db.utils import IntegrityError, DataError
from decimal import Decimal
import pytest


@pytest.mark.django_db
class TestProductModel:
    def test_basic_add(self):
        assert not Product.objects.all()
        Product(name='Product1', price=2.10, quantity_in_stock=3).save()
        assert Product.objects.count() == 1

    def test_name_uniqueness(self):
        assert not Product.objects.all()
        Product(name='Product1', price=2.10, quantity_in_stock=3).save()
        assert Product.objects.count() == 1

        with pytest.raises(IntegrityError) as e:
            Product(name='Product1', price=2.10, quantity_in_stock=3).save()
        assert 'duplicate key value violates unique constraint' in str(e)

    @pytest.mark.parametrize('name, exc',
                             [('Product1', None),
                              (None, IntegrityError),
                              ('a'*64, None),
                              ('a'*65, DataError),
                              ])
    def test_name_length_validation(self, name, exc):
        if exc:
            with pytest.raises(exc):
                Product(name=name, price=2.10, quantity_in_stock=3).save()
        else:
            Product(name=name, price=2.10, quantity_in_stock=3).save()

    @pytest.mark.parametrize('price, exc, expected_saved_price',
                             [(33.46, None, Decimal('33.46')),
                              (None, IntegrityError, None),
                              (33.463, None, Decimal('33.46')),
                              (22.1, None, Decimal('22.10')),
                              ])
    def test_price_validation(self, price, exc, expected_saved_price):
        if exc:
            with pytest.raises(exc):
                p = Product(name='Product1', price=price, quantity_in_stock=3)
                p.save()
        else:
            p = Product(name='Product1', price=price, quantity_in_stock=3)
            p.save()

        if expected_saved_price:
            p.refresh_from_db()
            assert p.price == expected_saved_price

    @pytest.mark.parametrize('quantity, exc',
                             [(33, None),
                              (-5, IntegrityError),
                              (0, None)
                              ])
    def test_name_quantity_validation(self, quantity, exc):
        if exc:
            with pytest.raises(exc):
                Product(name='Product1', price=2.10,
                        quantity_in_stock=quantity).save()
        else:
            Product(name='Product1', price=2.10,
                    quantity_in_stock=quantity).save()
