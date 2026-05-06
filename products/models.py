from django.db import models
from catalog.models import Categories
from django.utils.text import slugify
from unidecode import unidecode

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_color = models.CharField(max_length=7,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, default="Товар", verbose_name="Назва")
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Розмір")
    colors = models.ManyToManyField(Color, blank=True, verbose_name="Колір")
    description = models.TextField(blank=True, verbose_name="Опис")
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Зображення")
    range = models.IntegerField(default=0, verbose_name="Порядок")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    print_position_enabled = models.BooleanField(default=False)
    embroidery_enable = models.BooleanField(default=False)
    supports_stickers = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Знижка")
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
        verbose_name="Категорія"
    )
    class Status(models.TextChoices):
        IN_STOCK = "IN", "Є в наявності"
        PRE_ORDER = "PRE", "Передзамовлення"
        OUT_STOCK = "OUT", "Немає в наявності"

    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.IN_STOCK,
        verbose_name="Статус")


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

class Stickers(models.Model):
    name = models.CharField(max_length=50, default="Товар", verbose_name="Назва")
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Розмір")
    description = models.TextField(blank=True, verbose_name="Опис")
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Зображення")
    range = models.IntegerField(default=0, verbose_name="Порядок")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Знижка")
    class Status(models.TextChoices):
        IN_STOCK = "IN", "Є в наявності"
        PRE_ORDER = "PRE", "Передзамовлення"
        OUT_STOCK = "OUT", "Немає в наявності"

    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.IN_STOCK,
        verbose_name="Статус")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    @property
    def final_price(self, *args, **kwargs):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price