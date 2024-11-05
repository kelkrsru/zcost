from django.contrib import admin

import settings.models as settings_models


@admin.register(settings_models.SettingsPortal)
class SettingsPortalAdmin(admin.ModelAdmin):
    list_display = ('portal',)
