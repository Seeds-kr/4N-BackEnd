from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    folders = models.ManyToManyField(Folder, through='FolderLocation')
    # ManyToManyField : 다대다 관계
    # through='FolderLocation' 은 중개 모델 'FolderLocation'을 명시

    def __str__(self):
        return self.name


class FolderLocation(models.Model): # 중개 모델, Folder와 Location 간의 다대다 관계 관리
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.folder.name} - {self.location.name}"
