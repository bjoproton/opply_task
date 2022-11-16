# General
import pytest
import json
from rest_framework import status
from django.contrib.auth.models import User

# Opply
from store.models import Product


@pytest.fixture
def user():
    user = User.objects.create_user(username='test_user',
                                    password='test_password')
    user.save()
    return user


@pytest.fixture
def token(user, request_client):
    r = request_client.post('/auth/login/',
                            content_type='application/json',
                            data=json.dumps({'username': 'test_user',
                                             'password': 'test_password'}))
    return r.json()['token']


@pytest.fixture
def products():
    Product(name='Computer', price=2234.56, quantity_in_stock=33).save()
    Product(name='Chair', price=56, quantity_in_stock=21).save()
    Product(name='TV', price=345.11, quantity_in_stock=15).save()
    return Product.objects.all()


@pytest.mark.django_db
class TestProductView:
    api_path = '/store/products'

    def test_bad_auth(self, request_client, token):
        request_client.credentials(HTTP_AUTHORIZATION='Token ' + token[:-1])
        r = request_client.get(self.api_path,
                               content_type='application/json')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    def test_good_auth(self, request_client, token):
        request_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        r = request_client.get(self.api_path,
                               content_type='application/json')
        assert r.status_code == status.HTTP_200_OK

    def test_no_auth(self, request_client):
        r = request_client.get(self.api_path,
                               content_type='application/json')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    """ From now on there's no need to continue to explicitly
        supply auth credentials, as it's tested. We can now
        use force_authenicate on the user object.
    """

    def test_basic_response(self, request_client, user, products):
        request_client.logout()
        request_client.force_authenticate(user)

        r = request_client.get(self.api_path,
                               content_type='application/json')
        assert r.status_code == status.HTTP_200_OK
        expected_json = {
            "count": 3,
            "next": "http://testserver/store/products?page=2",
            "previous": None,
            "results": [
                {
                    "id": products[0].id,
                    "name": "Computer",
                    "price": '2234.56',
                    "quantity_in_stock": 33
                },
                {
                    "id": products[1].id,
                    "name": "Chair",
                    "price": "56.00",
                    "quantity_in_stock": 21
                }
            ]
        }
        assert r.json() == expected_json

        # Call the paginated page
        r = request_client.get(f'{self.api_path}?page=2',
                               content_type='application/json')
        expected_json = {
            "count": 3,
            "next": None,
            "previous": "http://testserver/store/products",
            "results": [
                {
                    "id": products[2].id,
                    "name": "TV",
                    "price": '345.11',
                    "quantity_in_stock": 15
                },
            ]
        }
        assert r.json() == expected_json
