from django.core.validators import FileExtensionValidator
from django.db import models

from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class VideoContentItem(ContentItem):
    _content_type = 'video'

    video = models.FileField(upload_to='videos',
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'])])
    muted = models.BooleanField(default=True)

    def extra_fields_dict(self):
        return {
            'sourceList': [self.video.url],
            'muted': self.muted
        }

    class Meta:
        verbose_name = 'video file'

    def __str__(self):
        return 'Video file: %s' % self.name


class VideoContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']
