import logging

from django.core.exceptions import BadRequest

import core.methods as core_methods

from django.conf import settings as app_settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from core.bitrix24.bitrix24 import create_portal, TaskB24

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
    logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')
    user_info = core_methods.get_current_user(request, auth_id, portal)
    logger.info(f'{NEW_STR}{user_info=}')

    task = TaskB24(portal, task_id)
    logger.info(f'{NEW_STR}{task.properties=}')

    context = {
        'title': title,
        'title_app': title_app,
    }

    return render(request, template, context)
