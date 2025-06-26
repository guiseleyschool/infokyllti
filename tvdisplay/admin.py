from datetime import timedelta
from django.utils.module_loading import import_string
from django.utils.timezone import now
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from tvdisplay.models import *


def file_to_class_name(filename):
    return ''.join(word.title() for word in filename.split('_'))


@admin.register(Display)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ('name','id','online','last_seen')
    readonly_fields = ('id','online','last_seen')

    def online(self, obj):
        active_timeline = now() - timedelta(minutes=15)
        try:
            return (obj.last_seen >= active_timeline)
        except TypeError:
            return False
    online.boolean = True


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name','valid_from','valid_to','override')
    fieldsets = (
        (
            None,
            {
                "fields": ["name", "content_items"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["valid_from", "valid_to", "override"],
            },
        ),
    )


class ContentItemChildAdmin(PolymorphicChildModelAdmin):
    list_display = ('name','display_seconds','valid_from','valid_to')
    base_model = ContentItem
    extra_fieldset_title = 'Content'
    base_fieldsets = (
        (
            None,
            {
                "fields": ["name", "display_seconds"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["valid_from", "valid_to", "font_family"],
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)


@admin.register(ContentItem)
class ContentItemParentAdmin(PolymorphicParentModelAdmin):
    list_display = ('name','display_seconds','valid_from','valid_to')
    base_model = ContentItem
    list_filter = (PolymorphicChildModelFilter,)

    def __init__(self, model, admin_site, *args, **kwargs):
        import pkgutil
        import os
        import content_items.types as ci

        child_content_items = [name for _, name, _ in pkgutil.iter_modules([os.path.dirname(ci.__file__)])]
        child_content_item_classes = []
        for content_item in child_content_items:
            ci_model = import_string(
                'content_items.types.%s.%sContentItem' % (content_item, file_to_class_name(content_item)))
            ci_admin = import_string(
                'content_items.types.%s.%sContentItemAdmin' % (content_item, file_to_class_name(content_item)))
            child_content_item_classes.append(ci_model)
            admin.site.register(ci_model, ci_admin)

        self.child_models = tuple(child_content_item_classes)
        super().__init__(model, admin_site, *args, **kwargs)
