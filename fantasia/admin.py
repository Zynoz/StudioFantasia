from django.contrib import admin

from fantasia.models import Post, GalleryImage, Message


list_display = ('image_tag', )


admin.site.register(Post)
admin.site.register(GalleryImage)
admin.site.register(Message)
