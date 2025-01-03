from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type='normal', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        print("printing the password set ",user.password)
        print("printing the user ")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, user_type='admin', **extra_fields)

 # Custom User Model
# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('admin', 'Admin'),
#         ('normal', 'Normal User')
#     )
#     username = None  # Remove username field
#     email = models.EmailField(unique=True)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
#     funds = models.FloatField(default=0.0)
#     last_login = models.DateTimeField(default=timezone.now)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return f"{self.email} ({self.user_type})"

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('normal', 'Normal User')
    )
    username = None  # Remove username field
    naam = models.CharField(max_length=10, null = True , default = 'No_Name')
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    funds = models.FloatField(default=0.0)
    last_login = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Define related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='tracker_user_set',  # Custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='tracker_user_permissions',  # Custom related_name
        blank=True
    )

    def __str__(self):
        return f"{self.email} ({self.user_type})"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

# Subcategory Model
class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.subcategory_name} ({self.category})"

# Expenses Model
import os
from django.conf import settings


class Expense(models.Model):
    PAYMENT_MODES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="expenses")
    description = models.CharField(max_length=255)
    transaction_image = models.ImageField(
        upload_to='transaction_images/', 
        null=True, 
        blank=True
    )
    bill_image = models.ImageField(
        upload_to='bill_images/', 
        null=True, 
        blank=True
    )
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODES)
    price = models.FloatField()
    quantity = models.FloatField()
    total_amount = models.FloatField(null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    expense_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super().save(*args, **kwargs)
        # Deduct funds after saving
        if self.user.user_type != 'admin':
            self.user.funds -= self.total_amount
            self.user.save()

    def __str__(self):
        return f"Expense: {self.description} by {self.user.email}"