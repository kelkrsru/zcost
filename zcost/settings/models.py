from django.db import models

from core.models import Portals


class SettingsPortal(models.Model):
    """Модель настроек портала"""

    portal = models.OneToOneField(Portals, verbose_name='Портал', related_name='settings_portal',
                                  on_delete=models.CASCADE, unique=True, db_index=True)
    cost_in_task_code = models.CharField('Код поля себестоимость в задачах', default='UF_AUTO_643983320441',
                                         max_length=30)
    cost_in_deal_code = models.CharField('Код поля себестоимость из задач',
                                         help_text='Код поля себестоимость из задач в сделках. Множественное поле.',
                                         default='UF_CRM_0000000000', max_length=30)
    ids_tasks_in_deal_code = models.CharField('Код поля ID задач',
                                              help_text='Код поля ID задач в сделках. Множественное поле.',
                                              default='UF_CRM_0000000000', max_length=30)
    links_tasks_in_deal_code = models.CharField('Код поля ссылки на задачи',
                                                help_text='Код поля ссылки на задачи в сделках. Множественное поле.',
                                                default='UF_CRM_0000000000', max_length=30)

    class Meta:
        verbose_name = 'Настройка портала'
        verbose_name_plural = 'Настройки портала'

        ordering = ['portal', 'pk']

    def __str__(self):
        return 'Настройки для портала {}'.format(self.portal.name)
