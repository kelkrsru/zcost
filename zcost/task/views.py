import decimal
import logging

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.urls import reverse_lazy

import core.methods as core_methods
import task.methods as task_methods

from django.conf import settings as app_settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from core.bitrix24.bitrix24 import create_portal, TaskB24, DealB24
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

    if not task_methods.check_fields(task, context, settings_portal, logger):
        logger.info(f'{SEPARATOR}')
        return render(request, template, context)

    context['form'] = CostForm()
    context['action_url'] = reverse_lazy('task:send-cost')

    return render(request, template, context)


@csrf_exempt
def send_cost(request):
    """Метод для обработки формы."""
    template = 'task/form_success.html'
    title = 'Задачи'
    title_app = app_settings.TITLE_APP

    context = {
        'title': title,
        'title_app': title_app,
    }

    logger.info(f'{NEW_STR}Запущена метод отправки себестоимости из задач')
    form = CostForm(request.POST)
    if form.is_valid():
        task_id = int(request.POST.get('task_id'))
        member_id = request.POST.get('member_id')
        logger.info(f'{NEW_STR}Переданные значения прошли валидацию')
        logger.info(f'{NEW_STR}{form.cleaned_data=}  {task_id=}  {member_id=}')

        portal = create_portal(member_id)
        settings_portal = get_object_or_404(SettingsPortal, portal=portal)
        logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')

        task = TaskB24(portal, task_id)
        logger.info(f'{NEW_STR}Получаем задачу по {task_id=}')
        logger.debug(f'{NEW_STR}{task.properties=}')
        deal_id = int(task.properties.get('ufCrmTask')[0].split('_')[1])
        deal = DealB24(portal, deal_id)
        logger.info(f'{NEW_STR}Получаем привязанную к задаче сделку по {deal_id=}')
        logger.debug(f'{NEW_STR}{deal.properties=}')

        fields = {settings_portal.cost_in_task_code: str(form.cleaned_data.get('cost'))}
        logger.info(f'{NEW_STR}Обновляем поля задачи {fields=}')
        result = task.update(fields)
        logger.info(f'{NEW_STR}Результат обновления полей задачи {result=}')

        cost_in_deal, ids_tasks_in_deal, links_tasks_in_deal = task_methods.check_fields_send_deal(task, deal, form,
                                                                                                   portal,
                                                                                                   settings_portal,
                                                                                                   logger)

        fields = {settings_portal.cost_in_deal_code: str(cost_in_deal),
                  settings_portal.ids_tasks_in_deal_code: ids_tasks_in_deal,
                  settings_portal.links_tasks_in_deal_code: links_tasks_in_deal}
        logger.info(f'{NEW_STR}Обновляем поля сделки {fields=}')
        result = deal.update(fields)
        logger.info(f'{NEW_STR}Результат обновления полей сделки {result=}')
        context['task_id'] = task_id
        context['deal_id'] = deal_id
        return render(request, template, context)
    return HttpResponse(404)



