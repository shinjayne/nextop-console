from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.KppPalletData)
admin.site.register(models.Code)
admin.site.register(models.PalletCode)
admin.site.register(models.Company)