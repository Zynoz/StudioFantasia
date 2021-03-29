from django.db import models
from django.utils.safestring import mark_safe


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=10000)
    pub_date = models.DateField('date published')
    image = models.ImageField(upload_to='postimages/', blank=True, null=True)

    def __str__(self):
        return self.title + ": " + self.content


class GalleryImage(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField('date published')
    img = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.img:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.img.url))
        return ""


class Message(models.Model):
    TYPE_CHOICES = (
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('info', 'info'),
        ('success', 'success'),
    )

    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='info')
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)

    def __str__(self):
        return "[" + self.type + "] " + self.title + ": " + self.text
