from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    saved_articles = models.ManyToManyField("Saved_Article", related_name="savers")

    def post_likes(self):
        return self.liked_posts.values_list('id', flat=True)

class Saved_Article(models.Model):
    title = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)
    url = models.URLField()
    img = models.URLField()
    publication_date = models.DateTimeField()
