from django.db import models
from django.utils.safestring import mark_safe


class Post(models.Model):
    title_de = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30)
    content_de = models.CharField(max_length=10000)
    content_en = models.CharField(max_length=10000)
    pub_date = models.DateField('date published')
    image = models.ImageField(upload_to='postimages/', blank=True, null=True)

    def __str__(self):
        return self.title_de + ": " + self.content_de

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="%s" width="100px" height="100px" />' % self.image.url)

    image_tag.short_description = 'Image'


class GalleryImage(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField('date published')
    img = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="%s" width="100px" height="100px" />' % self.img.url)

    image_tag.short_description = 'Image'


class Message(models.Model):
    TYPE_CHOICES = (
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('success', 'Success'),
    )

    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='Info')
    title_de = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30)
    text_de = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500)

    def __str__(self):
        return "[" + self.type + "] " + self.title_de + ": " + self.text_de
