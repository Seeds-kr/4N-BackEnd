from django.db import models
import requests


class Location(models.Model):
    # latitude = models.FloatField()  # 위도
    # longitude = models.FloatField() # 경도
    # name = models.CharField(max_length=100)
    id = models.CharField(max_length=50, primary_key=True)  # 카카오맵 API에서 제공하는 장소 ID
    name = models.CharField(max_length=255)                 # 장소 이름
    road_address_name = models.CharField(max_length=255)    # 도로명주소

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '장소'
        verbose_name_plural = '장소'
