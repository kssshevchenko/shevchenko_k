import pytest
from products.models import Product, Stickers
from django.urls import reverse

@pytest.mark.django_db
def test_add_to_cart(client):
    product = Product.objects.create(name= "Test", price=100)

    response = client.post(reverse('cart:add_products', kwargs={'product_id': 1}))
    assert response.status_code == 200

    cart = client.session.get("cart")
    assert cart is not None
    assert len(cart) == 1
    item = list(cart.values())[0]
    assert item["product_id"] == product.id

@pytest.mark.django_db
def test_custom_option(client):
    product = Product.objects.create(name="Test", price=100)
    data = {
        "id": 1,
        "color": "blue",
        "size": "M",
        "choices_embroidery": "YES"
    }

    client.post(reverse("cart:add_products", kwargs={"product_id": product.id}),
                data)

    cart = client.session.get("cart")
    item = list(cart.values())[0]

    assert item["color"] == "blue"
    assert item["size"] == "M"
    assert item["embroidery"] == "YES"

@pytest.mark.django_db
def test_changing_quantity(client):
    product = Product.objects.create(name="Test", price=100)
    data = {
        "id": 1,
        "color": "blue",
        "quantity": 1,
        "size": "M",
        "choices_embroidery": "YES"
    }
    client.post(
        reverse('cart:add_products', kwargs={'product_id': product.id}), data
    )

    cart = client.session.get("cart")
    assert cart is not None

    item_key = list(cart.keys())[0]
    client.post(reverse("cart:increase", kwargs={"key": item_key}), HTTP_REFERER="/cart/")
    updated_cart = client.session.get("cart")
    item = updated_cart[item_key]
    assert item["quantity"] == 2

    client.post(reverse("cart:decrease", kwargs={"key": item_key}), HTTP_REFERER="/cart/")
    updated_cart = client.session.get("cart")
    item = updated_cart[item_key]
    assert item["quantity"] == 1