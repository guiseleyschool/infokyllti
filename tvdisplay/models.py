from django.db import models
from polymorphic.models import PolymorphicModel
from sortedm2m.fields import SortedManyToManyField

from infokyllti.storage_backends import PrivateMediaStorage


class ContentItem(PolymorphicModel):
    _content_type = None

    name = models.CharField(max_length=100, unique=True)
    valid_from = models.DateTimeField(blank=True, null=True,
                                      help_text='If left blank, the content item is immediately valid.')
    valid_to = models.DateTimeField(blank=True, null=True,
                                    help_text='If left blank, the content item never expires.')
    background_image = models.ImageField(upload_to='backgrounds', blank=True, null=True)
    display_seconds = models.PositiveIntegerField(default=30, help_text='Seconds to display content item.')
    font_family = models.CharField(max_length=200, blank=True, null=True,
                                   help_text='Font name to override standard font. Must be installed on display.')

    def extra_fields_dict(self):
        return {}

    def to_dict(self):
        obj_dict = {
            'name': self.name,
            'displaySeconds': self.display_seconds,
            'contentType': self._content_type
        }

        if self.valid_from: obj_dict['validFrom'] = self.valid_from.isoformat()
        if self.valid_to: obj_dict['validTo'] = self.valid_to.isoformat()
        if self.background_image: obj_dict['backgroundImage'] = self.background_image.url
        if self.font_family: obj_dict['fontFamily'] = self.font_family

        return obj_dict | self.extra_fields_dict()

    def __str__(self):
        return 'Content item: %s' % self.name


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    valid_from = models.DateTimeField(blank=True, null=True,
                                      help_text='If left blank, the playlist is immediately valid.')
    valid_to = models.DateTimeField(blank=True, null=True,
                                    help_text='If left blank, the playlist never expires.')
    content_items = SortedManyToManyField(ContentItem, blank=True)

    def __str__(self):
        return 'Playlist: %s' % self.name


class Display(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)
    playlists = SortedManyToManyField(Playlist, blank=True)

    def __str__(self):
        return 'Display: %s (%s)' % (self.name, self.id)
