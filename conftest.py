import pytest
from rest_framework.test import APIClient


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker, django_db_createdb):
#     pass


@pytest.fixture
def request_client():
    return APIClient()
