from currencies.models import Currency
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MyAccountManager(BaseUserManager):
    def create_user(self, аты_жөні, тегі, username, электрондық_пошта, password=None):
        if not электрондық_пошта:
            raise ValueError('Сіздің электрондық пошта мекенжайыңыз міндетті болып табылады')
        if not username:
            raise ValueError('Пайдаланушы атыңыз міндетті болып табылады')
        user = self.model(
            электрондық_пошта=self.normalize_email(электрондық_пошта),
            username=username,
            аты_жөні=аты_жөні,
            тегі=тегі,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, аты_жөні, тегі, электрондық_пошта, username, password):
        user = self.create_user(
            электрондық_пошта=self.normalize_email(электрондық_пошта),
            username=username,
            password=password,
            аты_жөні=аты_жөні,
            тегі=тегі,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    аты_жөні = models.CharField(max_length=50)
    тегі = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    электрондық_пошта = models.EmailField(max_length=100, unique=True)
    телефон_нөмірі = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'электрондық_пошта'
    REQUIRED_FIELDS = ['username', 'аты_жөні', 'тегі']

    objects = MyAccountManager()

    def __str__(self):
        return self.электрондық_пошта

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE) 
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='profile')
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.аты_жөні

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
