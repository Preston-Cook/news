from django.contrib import admin
from .models import Saved_Article, User

# Register your models here.
admin.site.register(Saved_Article)
admin.site.register(User)