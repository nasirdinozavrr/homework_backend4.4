from django.db.models import Avg
from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def count_movies(self):
        return self.movies_all.all().count()



class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=100)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies_all')

    def __str__(self):
        return self.title

    @property
    def rating(self):
        z = 0
        for i in self.reviews.all():
            z += int(i.stars)
        return z/self.reviews.all().count()

class Review(models.Model):
    STARS = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    text = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True,
                              related_name='reviews')
    stars = models.PositiveSmallIntegerField(choices=STARS, null=True, blank=True)



    def __str__(self):
        return self.text
