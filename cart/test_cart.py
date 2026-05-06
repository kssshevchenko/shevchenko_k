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

# @pytest.mark.django_db
# def test_
