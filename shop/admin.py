from django.contrib import admin

from .models import CropDetail,contact,crop_recommend

admin.site.register(contact)
admin.site.register(crop_recommend)

@admin.register(CropDetail)
class CropDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'best_season', 'description')
    search_fields = ('name', 'best_season')
