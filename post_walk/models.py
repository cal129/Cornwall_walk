from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


class postwalk(models.Model):
    walk_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='walks')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    difficulty = models.IntegerField()
    type = models.IntegerField()
    distance = models.FloatField()
    time = models.DurationField()
    photo = CloudinaryField('image', default='placeholder')
    location = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    authorised = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
