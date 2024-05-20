from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class ImageContentItem(ContentItem):
    _content_type = 'image'

    class Meta:
        verbose_name = 'image'

    def __str__(self):
        return 'Image: %s' % self.name


class ImageContentItemAdmin(ContentItemChildAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['background_image'].label = 'Image'
        form.base_fields['background_image'].required = True
        return form
