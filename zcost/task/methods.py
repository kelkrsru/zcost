import decimal

SEPARATOR = '*' * 40
NEW_STR = '\n    '


def snake2camel(snake_str):
    """Метод преобразования названия поля из snake case в camel case."""
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def check_fields(task, context, settings_portal, logger):
    """Метод проверки полей в главном методе."""
    if 'ufCrmTask' not in task.properties or not task.properties.get('ufCrmTask'):
        # Задача не привязана к сделке
        logger.info(f'{NEW_STR}Задача не привязана к сделке.')
        context['error'] = 'Задача не привязана к сделке'
        return False
    if snake2camel(settings_portal.cost_in_task_code) not in task.properties:
        # Код поля Себестоимость в задачах указан неверно или не существует
        logger.info(f'{NEW_STR}Код поля "Себестоимость в задачах" указан неверно или не существует. '
                    f'{settings_portal.cost_in_task_code=}.')
        context['error'] = 'Код поля "Себестоимость в задачах" указан неверно или не существует.'
        return False
    if task.properties.get(snake2camel(settings_portal.cost_in_task_code)):
        # Поле Себестоимость в задачах уже заполнено
        logger.info(f'{NEW_STR}Поле "Себестоимость в задачах" уже заполнено. '
                    f'{task.properties.get(settings_portal.cost_in_task_code)=}.')
        context['error'] = (f'{NEW_STR}Поле "Себестоимость в задачах" уже заполнено. '
                            f'Себестоимость из задач = '
                            f'{task.properties.get(snake2camel(settings_portal.cost_in_task_code))}.')
        return False
    return True


def check_fields_send_deal(task, deal, form, portal, settings_portal, logger):
    """Метод проверки полей перед отправкой в сделку."""
    logger.info(f"{NEW_STR}")
    cost_in_deal = decimal.Decimal(0)
    if deal.properties.get(settings_portal.cost_in_deal_code):
        cost_in_deal = decimal.Decimal(deal.properties.get(settings_portal.cost_in_deal_code))
    logger.info(f"{NEW_STR}Формируем поле Себестоимость из задач. Полученное значение {cost_in_deal=}")
    cost_in_deal += form.cleaned_data.get('cost')
    logger.info(f"{NEW_STR}Вычисленное значение {cost_in_deal=}")

    ids_tasks_in_deal = []
    if deal.properties.get(settings_portal.ids_tasks_in_deal_code):
        ids_tasks_in_deal = deal.properties.get(settings_portal.ids_tasks_in_deal_code)
    logger.info(f"{NEW_STR}Формируем поле ID задач. Полученное значение {ids_tasks_in_deal=}")
    ids_tasks_in_deal.append(str(task.properties.get('id')))
    logger.info(f"{NEW_STR}Вычисленное значение {ids_tasks_in_deal=}")

    links_tasks_in_deal = []
    if deal.properties.get(settings_portal.links_tasks_in_deal_code):
        links_tasks_in_deal = deal.properties.get(settings_portal.links_tasks_in_deal_code)
    link = (f'https://{portal.name}{task.properties.get("responsible").get("link")}tasks/task/view/'
            f'{task.properties.get("id")}/')
    logger.info(f"{NEW_STR}Формируем поле Ссылки на задачи. Полученное значение {links_tasks_in_deal=}")
    links_tasks_in_deal.append(link)
    logger.info(f"{NEW_STR}Вычисленное значение {links_tasks_in_deal=}")

    return cost_in_deal, ids_tasks_in_deal, links_tasks_in_deal
