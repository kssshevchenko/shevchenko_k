from django.db import models




class Categories(models.Model):

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    parent_url = models.CharField(max_length=50)

    def __str__(self):
        return self.name