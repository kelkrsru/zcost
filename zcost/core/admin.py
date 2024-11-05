from django.contrib import admin

from core.models import Portals, Responsible


@admin.register(Portals)
class PortalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'member_id',
        'name',
        'auth_id_create_date',
    )


@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('id_b24', 'first_name', 'last_name')
