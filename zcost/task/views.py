import logging

from django.conf import settings as app_settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

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

    context = {
        'title': title,
        'title_app': title_app,
    }

    return render(request, template, context)
