from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

# Create your models here.



# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/board/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

# 포스트 모델
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = MarkdownxField()

    upload_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)
    upload_file = models.FileField(upload_to = 'blog/files/%Y/%m/%d', blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 삭제된 작성자는 None 으로 표시

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)



    def __str__(self):
        return f'[{self.pk}]{self.title} / 작성자 : {self.author}' # 작성자 추가

    def get_absolute_url(self):
        return f'/board/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     author = models.ForeignKey(User, on_delete=models.CASCADE)
     content = models.TextField()
     created_at = models.DateTimeField(auto_now_add = True)
     modified_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return f'{self.author}::{self.content}'

     def get_absolute_url(self):
         return f'{self.post.get_absolute_url()}#comment-{self.pk}'