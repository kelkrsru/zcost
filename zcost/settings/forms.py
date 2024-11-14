from django import forms

from .models import SettingsPortal


class SettingsPortalForm(forms.ModelForm):
    """Форма Настройки портала."""

    class Meta:
        model = SettingsPortal
        fields = ('cost_in_task_code', 'cost_in_deal_code', 'ids_tasks_in_deal_code', 'links_tasks_in_deal_code')
