from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


"""categories"""
class Categories(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

"""product items"""
class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="colors/",
                              blank=True, null=True,
                              verbose_name="Приклад кольору")

    def __str__(self):
        return self.name

class ProductType(models.Model):
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="producttype")
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

"""product main"""
class Product(models.Model):
    name = models.CharField(max_length=50, default="Товар", verbose_name="Назва")
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Розмір")
    colors = models.ManyToManyField(Color, blank=True, verbose_name="Колір")
    description = models.TextField(blank=True, verbose_name="Опис")
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL")
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL,default=1)
    is_sticker = models.BooleanField(default=False)
    range = models.IntegerField(default=0, verbose_name="Порядок")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    print_position_enabled = models.BooleanField(default=False)
    embroidery_enable = models.BooleanField(default=False)
    supports_stickers = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Знижка")
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Доплата за вишивку")
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
        default="Brooch",
        verbose_name="Категорія",
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

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/",
                              blank=True, null=True,
                              verbose_name="Зображення")