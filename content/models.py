from django.db import models
from products.models import Product
from django.utils.text import slugify
from unidecode import unidecode

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

class Pages(models.Model):
    class PagesType(models.TextChoices):
        DELIVERY = "delivery", "Доставка і оплата"
        CONTACTS = "contacts", "Контакти"
        SIZES = "sizes", "Розміри"
        TERMS = "terms", "Терміни виконання"

    name = models.CharField(blank=False, null=False, default="Інформація")
    description = models.TextField(blank=False, null=False, default="Детальна інформація")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    pages_type = models.CharField(
        unique=True,
        max_length=200,
        choices=PagesType.choices,
        default=PagesType.DELIVERY
    )
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.pages_type))
        super().save(*args, **kwargs)