from django.contrib import admin
from .models import BonusCard


class BonusCardAdmin(admin.ModelAdmin):
    list_display = ('series', 'number','release_date', 'activity_expires_date', 'activity_status')

admin.site.register(BonusCard, BonusCardAdmin)