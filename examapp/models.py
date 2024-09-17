from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
PLATFORM_CHOICES = (
    ('PS5', 'PlayStation 5'),
    ('Xbox One', 'Xbox One'),
    ('Switch', 'Nintendo Switch'),
    ('PC', 'Personal Computer'),
    ('Others', 'Others')
)

GENRE_CHOICES = (
    ('Shooter', 'Shooter'),
    ('Action', 'Action'),
    ('Adventure', 'Adventure'),
    ('RPG', 'Role-playing Game'),
    ('Others', 'Others')
)


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='Others')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='Others')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_in_stock = models.IntegerField(default=0)
    users_basket = models.ManyToManyField(User, related_name='basket', blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

