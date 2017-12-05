from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class AvocadoUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, date_of_birth, is_superuser=False ,password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            date_of_birth=date_of_birth,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, date_of_birth, password, **kwargs):
            user = self.create_user(
                email,
                first_name=first_name,
                last_name=last_name,
                username=username,
                date_of_birth=date_of_birth,
                password=password,
                is_superuser=True,
                **kwargs
            )
            user.is_admin = True
            user.save(using=self._db)
            return user




class AvocadoUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    username = models.CharField(max_length=70, unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return ('%s %s') % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    objects = AvocadoUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth']




class FileUploadHistory(models.Model):

    user = models.ForeignKey('AvocadoUser', on_delete=models.CASCADE)
    data = models.FileField(upload_to="sheets/%Y/%m/%d", null=True)
    weather= models.CharField(
        max_length=5,
        choices=(
        ('Use','Using weather data'),
        ('Not','Not using weather data')
        )
    )
    timestep= models.CharField(
        max_length=10,
        choices=(
            ('year','year'),
            ('month','month'),
            ('week','week'),
            ('day','day')
        )
    )

    def __str__(self):
        return str(self.id)


class PalletData(models.Model):

    date = models.DateTimeField()
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING, null=True)
    pallet_out = models.IntegerField()
    #pallet_in = models.IntegerField(null=True)
    code = models.CharField(null=True, max_length=10)
    manager = models.CharField(null=True, max_length=10)
    department = models.CharField(null=True, max_length=10)

    def __str__(self):
        return "id = " + str(self.id) + " : " + str(self.date) +" 수량 "+ str(self.pallet_out)




class Company(models.Model):

    name = models.CharField(null = True, max_length=30)

    def __str__(self):
        return "id = " + str(self.id) + " : " + str(self.name)



class PredictionHistory(models.Model):
    file_upload_history = models.ForeignKey('FileUploadHistory', on_delete=models.CASCADE, null=True)
    total_prediction = models.ForeignKey('TotalPrediction',  on_delete=models.DO_NOTHING, null=True)

class TotalPrediction(models.Model):

    date = models.DateField()
    total_pallet_out = models.IntegerField(null=True)
    #total_pallet_in = models.IntegerField(null=True)

