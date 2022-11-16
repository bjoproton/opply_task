import pytest
from rest_framework.test import APIClient


@pytest.fixture
def request_client():
    return APIClient()
