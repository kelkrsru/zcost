from django.conf import settings as app_settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from pybitrix24 import Bitrix24

from core.models import Portals
from settings.models import SettingsPortal


@xframe_options_exempt
@csrf_exempt
def install(request):
    """Метод установки приложения"""
    template = 'core/install.html'
    template_error = 'error.html'

    params = {
        'PLACEMENT': app_settings.PLACEMENT_APP,
        'HANDLER': app_settings.HANDLER_APP,
        'TITLE': app_settings.TITLE_APP,
        'DESCRIPTION': app_settings.DESCRIPTION_APP
    }

    try:
        portal: Portals = Portals.objects.get(member_id=request.POST['member_id'])
        portal.auth_id = request.POST['AUTH_ID']
        portal.refresh_id = request.POST['REFRESH_ID']
        portal.save()
    except Portals.DoesNotExist:
        portal: Portals = Portals.objects.create(member_id=request.POST['member_id'], name=request.GET.get('DOMAIN'),
                                                 auth_id=request.POST['AUTH_ID'], refresh_id=request.POST['REFRESH_ID'])
    SettingsPortal.objects.get_or_create(portal=portal)

    bx24 = Bitrix24(portal.name)
    bx24._access_token = portal.auth_id
    bx24._refresh_token = portal.refresh_id

    result = bx24.call('placement.bind', params)
    if 'error' in result:
        return render(request, template_error, {
            'error_name': result['error'],
            'error_description': result['error_description'],
        })

    context = {'title_app': app_settings.TITLE_APP}

    return render(request, template, context)
