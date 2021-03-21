from django.contrib import admin
from django.utils.html import format_html

from fantasia.models import Post, GalleryImage


# @admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.img.url))

    image_tag.short_description = 'Image'

    list_display = ['image_tag', ]


admin.site.register(Post)
admin.site.register(GalleryImage)
