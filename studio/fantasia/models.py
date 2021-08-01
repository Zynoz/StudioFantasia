from django.db import models


class Post(models.Model):
    title_de = models.CharField(max_length=30, default='')
    title_en = models.CharField(max_length=30, default='')
    content_de = models.CharField(max_length=10000, default='')
    content_en = models.CharField(max_length=10000, default='')
    pub_date = models.DateField('date published')
    url = models.CharField(max_length=10000)
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
    title_de = models.CharField(max_length=30, default='')
    title_en = models.CharField(max_length=30, default='')
    text_de = models.CharField(max_length=500, default='')
    text_en = models.CharField(max_length=500, default='')

    def __str__(self):
        return "[" + self.type + "] " + self.title_de + ": " + self.text_de

# class UploadBackupForm(forms.Form):
#     backup = forms.FileField()
