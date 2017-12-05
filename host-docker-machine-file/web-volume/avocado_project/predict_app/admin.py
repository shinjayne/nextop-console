from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.AvocadoUser)
admin.site.register(models.FileUploadHistory)
admin.site.register(models.PalletData)
admin.site.register(models.PredictionHistory)
admin.site.register(models.TotalPrediction)
admin.site.register(models.Company)