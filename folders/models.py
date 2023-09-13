from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locations = models.ManyToManyField('locations.Location')
    created = models.DateTimeField(auto_now_add=True)  # 생성한 날짜와 시각
    updated = models.DateTimeField(auto_now=True)  # 업데이트한 날짜와 시각

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '폴더'
        verbose_name_plural = '폴더'
        ordering = ['-updated']   # 업데이트 날짜 역순으로 정렬. 최근에 업데이트 된 폴더가 상단에 표시됨.

    @classmethod
    def create_folder(cls, name, user):
        folder = cls(name=name, user=user)
        folder.save()
        return folder
