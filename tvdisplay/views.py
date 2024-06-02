import json

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.db.models import Q
from django.utils.timezone import now
from .models import Display


validity_filter = Q(
    (Q(valid_from__isnull=True) | Q(valid_from__lte=now()))
    & (Q(valid_to__isnull=True) | Q(valid_to__gte=now()))
)


def home(request):
    return render(request, 'tvdisplay/home.html')


def display_view(request):
    return render(request, 'tvdisplay/display.html')


def default_config(request):
    return render(request, 'tvdisplay/default_config.json')


def display_config(request, display_id):
    try:
        display = Display.objects.get(pk=display_id)

        if display.playlists.count() == 0:
            return render(request, 'tvdisplay/default_config.json')

        display_content = {
            'displayDefaults': {
                'remoteURL': static('')
            },
            'contentList': []
        }

        for playlist in display.playlists.filter(validity_filter).all():
            for ci in playlist.content_items.filter(validity_filter).all():
                display_content['contentList'].append(ci.to_dict())

        return HttpResponse(json.dumps(display_content), content_type='application/json')
    except Display.DoesNotExist:
        display = Display(pk=display_id, name='Discovered Display %s' % display_id)
        display.save()
        raise Http404("Display not found")
