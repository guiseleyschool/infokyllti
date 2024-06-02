from django.contrib import admin
from django.db import models

from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class ImageListContentItem(ContentItem):
    _content_type = 'imageList'

    slide_display_seconds = models.PositiveIntegerField(default=10,
                                                        help_text='Number of seconds to display each slide.')

    class Meta:
        verbose_name = 'image list'

    def __str__(self):
        return 'Image list: %s' % self.name

    def extra_fields_dict(self):
        return {
            'backgroundImages': [item.image.url for item in self.imagelistitem_set.all()],
            'slideSeconds': self.slide_display_seconds,
            'displaySeconds': None
        }


class ImageListItem(models.Model):
    content_item = models.ForeignKey(ImageListContentItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_list_images')
    priority = models.PositiveSmallIntegerField(default=0)


class ImageListItemInline(admin.TabularInline):
    model = ImageListItem


class ImageListContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']
    inlines = [ImageListItemInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['display_seconds'].widget = HiddenInput()
        return form
