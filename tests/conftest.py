import pytest
from rest_framework.test import APIClient
from model_bakery import baker




@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return baker.make('shops.User', **kwargs)

    return factory


@pytest.fixture
def confirm_email_token_factory():
    def factory(**kwargs):
        return baker.make('shops.ConfirmEmailToken', **kwargs)

    return factory


@pytest.fixture
def shop_factory():
    def factory(**kwargs):
        return baker.make('shops.Shop', **kwargs)

    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('shops.Order', **kwargs)

    return factory


@pytest.fixture
def order_item_factory():
    def factory(**kwargs):
        return baker.make('shops.OrderItem', **kwargs)

    return factory


@pytest.fixture
def product_info_factory():
    def factory(**kwargs):
        return baker.make('shops.ProductInfo', **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('shops.Product', **kwargs)

    return factory


@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('shops.Category', **kwargs)

    return factory


@pytest.fixture
def contact_factory():
    def factory(**kwargs):
        return baker.make('shops.Contact', **kwargs)

    return factory




