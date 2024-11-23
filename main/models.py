from django.db import models
from django.contrib.auth.models import AbstractUser

class Project(models.Model):
    statuses = (('In Working', 'В разработке'),
                ('In planeted', 'Запланирован'),
                ('Freeze', 'Заморожен'),
                ('Ready', 'Завершен'))
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=35, choices=statuses)

class User(AbstractUser):
    role = models.CharField(max_length=50)
    avatar = models.ImageField(default='media/avatar.png')
    projects = models.ManyToManyField(Project)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Уникальное имя для обратного доступа
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Уникальное имя для обратного доступа
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )








class Task(models.Model):
    statuses = (('Active', 'Активен'),
                ('Archived', 'Архивирован'))
    
    priorities = (('Low', 'Низкий'),
                ('Medium', 'Средний'),
                ('High', 'Высокий'))

    title = models.CharField(max_length=50)
    content = models.TextField()
    project = models.ManyToManyField(Project)
    user = models.ManyToManyField(User)

    status = models.CharField(max_length=35, choices=statuses)
    priority = models.CharField(max_length=40, choices=priorities)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    dead_line = models.DateField()
    tester = models.CharField(max_length=50)
