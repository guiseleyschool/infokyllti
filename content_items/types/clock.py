from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class ClockContentItem(ContentItem):
    _content_type = 'clock'

    class Meta:
        verbose_name = 'clock'

    def __str__(self):
        return 'Clock: %s' % self.name


class ClockContentItemAdmin(ContentItemChildAdmin):
    pass
