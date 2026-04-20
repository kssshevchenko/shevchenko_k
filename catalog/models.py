from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Categories(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    parent_url = models.CharField(max_length=50)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)
