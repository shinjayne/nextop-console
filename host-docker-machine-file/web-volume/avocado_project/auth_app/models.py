from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class NextopUserManager(BaseUserManager):
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




class NextopUser(AbstractBaseUser, PermissionsMixin):
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

    objects = NextopUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth']
