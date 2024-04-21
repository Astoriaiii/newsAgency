from django.db import models

# Create your models here.
class StoryModel(models.Model):
    CATEGORY_CHOICES = (
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    )

    REGION_CHOICES = (
        ('uk', 'UK'),
        ('eu', 'Europe'),
        ('w', 'World'),
    )

    uniqueKey= models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    author = models.CharField(max_length=100)
    date = models.DateField()
    details = models.CharField(max_length=128)

class user(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)