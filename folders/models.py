from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    locations = models.ManyToManyField('locations.Location')

    def __str__(self):
        return self.name
