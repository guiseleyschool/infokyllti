from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin
from django_prose_editor.fields import ProseEditorField
from django.db import models


class HtmlContentItem(ContentItem):
    _content_type = 'html'

    body = ProseEditorField()

    def extra_fields_dict(self):
        return {'innerHTML': self.body}

    class Meta:
        verbose_name = 'HTML page'

    def __str__(self):
        return 'HTML page: %s' % self.name


class HtmlContentItemAdmin(ContentItemChildAdmin):
    pass
