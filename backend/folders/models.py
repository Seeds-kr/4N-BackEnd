from django.db import models
from accounts.models import User
from place.models import Places


class Folder(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Places, blank=True)  # 폴더 생성 시점에 선택하지 않아도 되도록 blank=True 옵션 추가
    created = models.DateTimeField(auto_now_add=True)  # 생성한 날짜와 시각
    updated = models.DateTimeField(auto_now=True)  # 업데이트한 날짜와 시각

    def __str__(self):
        return self.title
    
    class Meta: 
        db_table = 'folders_folder'
        verbose_name = '폴더'
        verbose_name_plural = '폴더'
