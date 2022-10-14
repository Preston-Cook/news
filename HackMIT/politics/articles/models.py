from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    saved_articles = models.ManyToManyField("Saved_Article", related_name="savers")

class Saved_Article(models.Model):
    title = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)
    url = models.URLField()
    img = models.URLField()
    publication_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title}: {self.publication_date}"
