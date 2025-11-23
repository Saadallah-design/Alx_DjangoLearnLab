from django.db import models
from django.conf import settings

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=65)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
        )

    def __str__(self):
        return self.title