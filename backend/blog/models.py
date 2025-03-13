from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(_('title'), max_length=255)
    content = RichTextField(_('content'))
    image = models.ImageField(_('image'), upload_to='images/', blank=True, null=True)
    video = models.FileField(_('video'), upload_to='videos/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title