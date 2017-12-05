from django.forms import ModelForm

from . import models




class FileUploadHistoryForm(ModelForm):
    class Meta :
        model = models.FileUploadHistory
        fields = ('user','data', 'weather', 'timestep')

