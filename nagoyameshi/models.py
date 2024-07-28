from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    budget = models.PositiveIntegerField()
    information = models.TextField()
    img = models.ImageField(blank=True, default='noImage.png')

    def __str__(self):
        return self.name
