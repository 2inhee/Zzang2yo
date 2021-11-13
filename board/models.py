from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.



class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()

    upload_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)
    upload_file = models.FileField(upload_to = 'blog/files/%Y/%m/%d', blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 삭제된 작성자는 None 으로 표시

    def __str__(self):
        return f'[{self.pk}]{self.title} / 작성자 : {self.author}' # 작성자 추가

    def get_absolute_url(self):
        return f'/board/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]