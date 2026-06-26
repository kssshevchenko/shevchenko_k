import pytest
from orders.models import Order
from django.urls import reverse

@pytest.mark.django_db
def test_create_order(client):
    response = client.get(reverse("checkout:create_order"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_order_items(client):
    data = {
        "name": "Test",
        "email": "test@test.ts",
        "last_name": "Test",
        "phone": 12345,
    }
    response = client.post(reverse("checkout:create_order"), data)

    assert response.status_code == 200
    assert client.session.get("cart") == {}

@pytest.mark.django_db
def test_wrong_items(client):

    data = {
        "name": "Test",
        "email": "test_test.ts",
        "last_name": "Test",
        "phone": 1,
    }
    response = client.post(reverse("checkout:create_order"), data)

    assert response.status_code == 400
    assert Order.objects.count() == 0
