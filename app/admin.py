from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(action_master)
class action_master_admin(admin.ModelAdmin):
    list_display = ('id', 'note', 'description', 'lead_time', 'type')

admin.site.register(provider_master)

@admin.register(appeal_master)
class appeal_master_admin(admin.ModelAdmin):
    list_display = ('case_number', 'structure', 'appeal_name')
