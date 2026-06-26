from django.db import models
from products.models import Product

class Blocks(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="content/",
                              blank=True, null=True,)
    products = models.ManyToManyField(Product)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name
