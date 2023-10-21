from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=64)
    useremail = models.EmailField(max_length=64)
    password = models.CharField(max_length=128) # 해싱 때문에 128글자로 늘렸습니다. -서하-
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

    class Meta: 
        db_table = 'accounts_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
    


