from django.conf import settings as app_settings
from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

import core.methods as core_methods
from core.bitrix24.bitrix24 import create_portal
from settings.forms import SettingsPortalForm
from settings.models import SettingsPortal


@xframe_options_exempt
@csrf_exempt
def index(request):

    template = 'settings/index.html'
    title = 'Настройки приложения'
    title_app = app_settings.TITLE_APP

    auth_id = ''

    try:
        member_id = core_methods.check_request(request)
    except BadRequest:
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })
    portal = create_portal(member_id)
    settings_portal, created = SettingsPortal.objects.get_or_create(portal=portal)
    user_info = core_methods.get_current_user(request, auth_id, portal)

    if 'AUTH_ID' in request.POST:
        form = SettingsPortalForm(instance=settings_portal)
    else:
        form = SettingsPortalForm(request.POST or None, instance=settings_portal)
        if form.is_valid():
            fields_form = form.save(commit=False)
            fields_form.portal = portal
            fields_form.save()

    context = {
        'title': title,
        'title_app': title_app,
        'member_id': member_id,
        'user': user_info,
        'form': form,
        'action_url': reverse_lazy("settings:index")
    }
    response = render(request, template, context)
    if auth_id:
        response.set_cookie(key='user_id', value=user_info.get('user_id'))
    return response
