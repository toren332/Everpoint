from django.contrib import admin
from . import models

admin.site.register(models.XlsxFile)


@admin.register(models.LatLngHistory)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


@admin.register(models.Ship)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
