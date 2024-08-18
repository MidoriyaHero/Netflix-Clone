from django.db import models
import uuid
from django.conf import settings
# Create your models here.
class Movie(models.Model):
    GENRE_CHOICES = [
        ('action','Action'),
        ('comedy','Comedy'),
        ('roman','Roman'),
        ('fantasy','Fantasy'),
        ('science_fiction','Science Fiction'),
        ('drama','Drama'),
        ('horror','Horror'),
    ]
    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=256)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField() 
    image_card = models.ImageField(upload_to='movie_image/')
    image_cover = models.ImageField(upload_to='movie_image/')
    video = models.FileField(upload_to='movie_video/')
    movie_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title