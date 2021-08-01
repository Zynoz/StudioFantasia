from django.contrib import admin

from .models import Post, GalleryImage, Message#, UploadBackupForm

list_display = ('image_tag', )


admin.site.register(Post)
admin.site.register(GalleryImage)
admin.site.register(Message)
# admin.site.register(UploadBackupForm)