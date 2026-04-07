from django.db import models
from catalog.models import Categories
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=50, default="Товар")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    order = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True
    )


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)
