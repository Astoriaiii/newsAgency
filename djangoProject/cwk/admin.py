from django.contrib import admin

# Register your models here.
from .models import StoryModel
from .models import user

admin.site.register(StoryModel)
admin.site.register(user)

