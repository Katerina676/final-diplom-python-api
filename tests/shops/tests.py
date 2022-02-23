import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from shops.models import User


@pytest.mark.django_db
def test_user_create(api_client):
    some_user = {
        "first_name": "A",
        "last_name": "test",
        "email": "test@gmail.com",
        "password": "13656vbvffvf",
        "company": "Yandex",
        "position": "Assesor"
    }

    url = reverse("shops:user-register")
    resp = api_client.post(url, data=some_user)

    assert resp.status_code == HTTP_201_CREATED
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_confirm(api_client, user_factory, confirm_email_token_factory):
    user = user_factory()
    tok = confirm_email_token_factory()
    user.confirm_email_tokens.add(tok)
    url = reverse("shops:user-register-confirm")
    resp = api_client.post(url, data={"email": user.email, "token": "wrong_key"})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is False
    resp = api_client.post(url, data={"email": user.email, "token": tok.key})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_login(api_client, user_factory):
    mail = "test@gmail.com"
    passw = "cdjndcbdbcdh12345"

    some_user = {
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "email": mail,
        "password": passw,
        "company": "Yandex",
        "position": "Specialist"
    }

    url = reverse("shops:user-register")
    resp = api_client.post(url, data=some_user)
    assert resp.json().get('Status') is True

    user = User.objects.get(email=mail)
    user.is_active = True
    user.save()

    url = reverse("shops:user-login")
    resp = api_client.post(url, data={"email": mail, "password": passw})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_user_details(api_client, user_factory):
    url = reverse("shops:user-details")
    user = user_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    api_client.force_authenticate(user=user)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('email') == user.email
    api_client.post(url, data={
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@mail.com",
        "password": "1234fvfvfvf",
        "company": "Company122",
        "position": "Position123"
    })
    resp = api_client.get(url)
    assert resp.json().get('company') == "Company122"
    resp = api_client.post(url, data={"type": "shop"})
    resp = api_client.get(url)
    assert resp.json().get('type') == "shop"


@pytest.mark.django_db
def test_user_contacts(api_client, user_factory):
    url = reverse("shops:user-contact")
    user = user_factory()
    api_client.force_authenticate(user=user)
    contact = {
        "city": "Moscow",
        "street": "Some str.",
        "phone": "+789456123"
    }

    resp = api_client.post(url, data=contact)
    assert resp.status_code == HTTP_201_CREATED
    resp = api_client.get(url)
    for entry in list(contact.keys()):
        assert resp.json()[0].get(entry) == contact.get(entry)
    client = user.contacts.first().id

    resp = api_client.put(url, data={"building": "1", "id": client})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True
    assert user.contacts.get(id=client).building == '1'

    resp = api_client.delete(url, data={"items": client})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_products(api_client, user_factory, shop_factory, order_factory,
                  product_info_factory, product_factory, category_factory):

    url = reverse("shops:shops")
    shop = shop_factory()
    customer = user_factory()
    category = category_factory()
    prod = product_factory(category=category)
    prod_info = product_info_factory(product=prod, shop=shop)
    api_client.force_authenticate(user=customer)
    shop_id = shop.id
    category_id = category.id
    resp = api_client.get(url, shop_id=shop.id, category_id=category.id)
    assert resp.status_code == HTTP_200_OK
    assert resp.json()[0].get('id', False)


@pytest.mark.django_db
def test_partner_upload(api_client, user_factory):
    price = 'https://raw.githubusercontent.com/mexalon/finproj/master/mymazon/data_for_ulpoad/shop1.yml'
    url = reverse("shops:partner-update")
    u = user_factory()
    api_client.force_authenticate(user=u)

    resp = api_client.post(url, data={"url": price})
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert resp.json().get('Status') is False

    resp = api_client.post(reverse("shops:user-details"), data={"type": "shop"})
    resp = api_client.get(reverse("shops:user-details"))
    assert resp.json().get('type') == "shop"

    resp = api_client.post(url, data={"url": price})
    assert resp.status_code == HTTP_200_OK
    assert resp.json().get('Status') is True


@pytest.mark.django_db
def test_category_get(api_client, category_factory):
    url = reverse('shops:categories')
    category_factory(_quantity=4)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 4



@pytest.mark.django_db
def test_basket_post_by_anonymous_user(api_client):
    payload = {"items": [{"product_info": 1, "quantity": 2}]}
    url = reverse('shops:basket')
    response = api_client.post(url, data=payload)
    assert response.status_code == HTTP_401_UNAUTHORIZED



