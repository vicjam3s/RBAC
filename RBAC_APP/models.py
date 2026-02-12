from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

#Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have is_staff true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super user must have is_super true')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True, unique=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# RBAC Models for Blog
class Role(models.Model):
    """Blog Roles: Reader, Editor, Author"""
    READER = 'reader'
    EDITOR = 'editor'
    AUTHOR = 'author'
    
    ROLE_CHOICES = [
        (READER, 'Reader'),
        (EDITOR, 'Editor'),
        (AUTHOR, 'Author/Admin'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class UserRole(models.Model):
    """Association between User and Role"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
    
    def __str__(self):
        return f"{self.user.email} - {self.role.get_name_display()}"


class Post(models.Model):
    """Blog Post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title