from django.core.validators import FileExtensionValidator
from django.db import models
from django.forms import HiddenInput

from tvdisplay.models import ContentItem
from tvdisplay.admin import ContentItemChildAdmin


class PdfContentItem(ContentItem):
    _content_type = 'pdf'

    pdf_file = models.FileField(upload_to='pdfs',
                                validators=[
                                    FileExtensionValidator(allowed_extensions=['pdf'])],
                                verbose_name='PDF file')
    slide_display_seconds = models.PositiveIntegerField(default=10,
                                                        help_text='Number of seconds to display each slide.')

    def extra_fields_dict(self):
        return {
            'pdfFile': self.pdf_file.url,
            'slideSeconds': self.slide_display_seconds,
            'displaySeconds': None
        }

    class Meta:
        verbose_name = 'PDF file'

    def __str__(self):
        return 'PDF file: %s' % self.name


class PdfContentItemAdmin(ContentItemChildAdmin):
    exclude = ['background_image']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['display_seconds'].widget = HiddenInput()
        return form
