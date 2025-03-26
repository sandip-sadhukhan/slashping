import datetime
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    

def user_directory_path(instance, filename): 
	return 'profile_images/user_{0}/{1}'.format(instance.id, filename) 

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=150)
    reminder_email_time = models.TimeField(default=datetime.time(hour=8, minute=0))
    new_client_target = models.PositiveIntegerField(default=0, validators = [MinValueValidator(0)])
    new_client_in_days = models.PositiveIntegerField(default=7, validators = [MinValueValidator(1), MaxValueValidator(30)])
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        sep = self.name.split(" ")

        return sep[0] if sep else self.name

