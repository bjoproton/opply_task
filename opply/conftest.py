import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default']['NAME'] = f'test_{settings.DATABASES["default"]["NAME"]}'
