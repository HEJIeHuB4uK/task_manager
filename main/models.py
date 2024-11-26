from django.db import models
from django.contrib.auth.models import AbstractUser


class Project(models.Model):
    statuses = (
        ("In Working", "В разработке"),
        ("In Planeted", "Запланирован"),
        ("Freeze", "Заморожен"),
        ("Ready", "Завершен"),
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=35, choices=statuses, default="In Planeted")


class User(AbstractUser):
    password = models.CharField(max_length=1024)
    role = models.CharField(max_length=50)
    avatar = models.ImageField(default="media/avatar.png")
    projects = models.ManyToManyField(Project)


class Task(models.Model):
    statuses = (("Active", "Активен"), ("Archived", "Архивирован"))

    priorities = (("Low", "Низкий"), ("Medium", "Средний"), ("High", "Высокий"))

    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    project = models.ManyToManyField(Project)
    user = models.ManyToManyField(User, blank=True)

    status = models.CharField(max_length=35, choices=statuses)
    priority = models.CharField(max_length=40, choices=priorities)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    dead_line = models.DateField()
    tester = models.CharField(max_length=50, blank=True)
