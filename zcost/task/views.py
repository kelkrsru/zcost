import logging

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.urls import reverse_lazy

import core.methods as core_methods

from django.conf import settings as app_settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from core.bitrix24.bitrix24 import create_portal, TaskB24
from settings.models import SettingsPortal
from task.forms import CostForm

logger = logging.getLogger(__name__)
SEPARATOR = '*' * 40
NEW_STR = '\n    '


@xframe_options_exempt
@csrf_exempt
def index(request):
    """Метод страницы Карточка сделки."""
    template = 'task/index.html'
    title = 'Задачи'
    title_app = app_settings.TITLE_APP

    logger.info(f'{SEPARATOR}')
    logger.info(f'{NEW_STR}{request.method=}  {request.build_absolute_uri()}')

    try:
        member_id, task_id, auth_id = core_methods.initial_check(request, entity_type='task_id',
                                                                 placement_id_code='taskId')
        logger.debug(f'{NEW_STR}{member_id=}  {task_id=}  {auth_id=}')
    except BadRequest:
        logger.error(f'{NEW_STR}Неизвестный тип запроса {request.method=}')
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })

    portal = create_portal(member_id)
    settings_portal = get_object_or_404(SettingsPortal, portal=portal)
    logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')
    user_info = core_methods.get_current_user(request, auth_id, portal)
    logger.info(f'{NEW_STR}{user_info=}')

    task = TaskB24(portal, task_id)
    logger.info(f'{NEW_STR}{task.properties=}')

    context = {
        'title': title,
        'title_app': title_app,
        'member_id': member_id,
        'task_id': task_id,
    }

    if 'ufCrmTask' not in task.properties or not task.properties.get('ufCrmTask'):
        # Задача не привязана к сделке
        logger.info(f'{NEW_STR}Задача не привязана к сделке.')
        logger.info(f'{SEPARATOR}')
        context['error'] = 'Задача не привязана к сделке'
        return render(request, template, context)
    if snake2camel(settings_portal.cost_in_task_code) not in task.properties:
        # Код поля Себестоимость в задачах указан неверно или не существует
        logger.info(f'{NEW_STR}Код поля "Себестоимость в задачах" указан неверно или не существует. '
                    f'{settings_portal.cost_in_task_code=}.')
        logger.info(f'{SEPARATOR}')
        context['error'] = 'Код поля "Себестоимость в задачах" указан неверно или не существует.'
        return render(request, template, context)
    if task.properties.get(snake2camel(settings_portal.cost_in_task_code)):
        # Поле Себестоимость в задачах уже заполнено
        logger.info(f'{NEW_STR}Поле "Себестоимость в задачах" уже заполнено. '
                    f'{task.properties.get(settings_portal.cost_in_task_code)=}.')
        logger.info(f'{SEPARATOR}')
        context['error'] = (f'{NEW_STR}Поле "Себестоимость в задачах" уже заполнено. '
                            f'{task.properties.get(settings_portal.cost_in_task_code)=}.')
        return render(request, template, context)

    context['form'] = CostForm()
    context['action_url'] = reverse_lazy('task:send-cost')

    return render(request, template, context)


@csrf_exempt
def send_cost(request):
    """Метод для обработки формы."""
    logger.info(f'')
    form = CostForm(request.POST)
    if form.is_valid():
        logger.debug(f'{NEW_STR}{form.cleaned_data=}')
        task_id = form.cleaned_data.get('task_id')
        member_id = form.cleaned_data.get('member_id')
        portal = create_portal(member_id)
        settings_portal = get_object_or_404(SettingsPortal, portal=portal)
        logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')

        task = TaskB24(portal, task_id)
        return HttpResponse(task)
    return HttpResponse(404)


def snake2camel(snake_str):
    """Метод преобразования названия поля из snake case в camel case."""
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])
