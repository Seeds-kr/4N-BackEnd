from django.db import models
from accounts.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False)
    content = models.TextField(null=False)
    image = models.ImageField(upload_to='', blank=True, null=True )  # 이미지 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 