from django.db import models
from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class YoutubeContentItem(ContentItem):
    _content_type = 'youtube'

    video_id = models.CharField(max_length=30, help_text="YouTube video ID from after ?v= in URL")

    def extra_fields_dict(self):
        return {'video_id': self.video_id}

    class Meta:
        verbose_name = 'YouTube video'

    def __str__(self):
        return 'YouTube: %s' % self.name


class YoutubeContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']
