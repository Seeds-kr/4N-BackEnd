from django.db import models


class Location(models.Model):
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField() # 경도
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '장소'
        verbose_name_plural = '장소'
