from django.db import models
from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class IframeContentItem(ContentItem):
    _content_type = 'iframe'

    source = models.URLField(help_text="The URL of the content item.")

    def extra_fields_dict(self):
        return {'source': self.source}

    class Meta:
        verbose_name = 'iFrame'

    def __str__(self):
        return 'iFrame: %s' % self.name


class IframeContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']
