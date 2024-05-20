from django.contrib import admin
from django.db import models

from infokyllti.storage_backends import PrivateMediaStorage
from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class ImageListContentItem(ContentItem):
    _content_type = 'imageList'

    class Meta:
        verbose_name = 'image list'

    def __str__(self):
        return 'Image list: %s' % self.name

    def extra_fields_dict(self):
        return {
            'backgroundImages': [item.image.url for item in self.imagelistitem_set.all()]
        }


class ImageListItem(models.Model):
    content_item = models.ForeignKey(ImageListContentItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_list_images', storage=PrivateMediaStorage())
    priority = models.PositiveSmallIntegerField(default=0)


class ImageListItemInline(admin.TabularInline):
    model = ImageListItem


class ImageListContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']
    inlines = [ImageListItemInline]
