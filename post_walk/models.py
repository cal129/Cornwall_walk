from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class postwalk(models.Model):
    WALK_TYPES = [
        (0, 'Circular'),
        (1, 'Out and Back'),
        (2, 'One Way'),
    ]

    DIFFICULTY_CHOICES = [
        (0, 'Easy'),
        (1, 'Moderate'),
        (2, 'Hard'),
        (3, 'Expert'),
    ]

    walk_id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='walks')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=0)
    type = models.IntegerField(choices=WALK_TYPES)
    distance = models.FloatField(validators=[MinValueValidator(0)])
    time_hours = models.IntegerField(validators=[MinValueValidator(0)])
    time_minutes = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    photo = CloudinaryField('image', default='placeholder')
    location = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    authorised = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
