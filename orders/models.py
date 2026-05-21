from django.db import models

from products.models import Product


class Order(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    country = models.CharField(max_length=50, default=1)
    city = models.CharField(max_length=50, default=1)
    street = models.CharField(max_length=100, default=1)
    building = models.CharField(max_length=10, default=1)
    office = models.CharField(max_length=10, default=1)
    entrance = models.CharField(max_length=10, default=1)
    region = models.CharField(max_length=10, default=1)
    zip_code = models.CharField(max_length=10, default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Payment(models.TextChoices):
        PRERAID = "PRE", "Оплата на реквізити",
        POSTPAID = "POST", "Оплата при отриманні"

    payment = models.CharField(
        max_length=10,
        choices=Payment.choices,
        default=Payment.PRERAID,
        verbose_name="Спосіб оплати"
    )

    def __str__(self):
        return f"Order {self.id}"

    def total_price(self):
        return sum(item.get_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    product_name = models.CharField(max_length=20, default="Product")
    sizes = models.CharField(max_length=10, blank=True, null=True, verbose_name="Розмір")
    count_sticker = models.CharField(
        max_length=20,
        choices=[(1, "1 принт"), (3, "3 принти"),],
        null=True,
        blank=True
    )

    sticker_position = models.CharField(
        max_length=20,
        choices=[("FRONT", "Спереду"), ("BACK", "Ззаду")],
        null=True,
        blank=True
    )

    embroidery = models.CharField(
        max_length=20,
        choices=[("YES", "З вишивкою"), ("NO", "Без вишивки")],
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.id)

    def get_price(self):
        return self.price * self.quantity