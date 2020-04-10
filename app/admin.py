from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(action_master)

class action_master_admin(admin.ModelAdmin):
    list_display = ('id','note','description', 'lead_time', 'type')
