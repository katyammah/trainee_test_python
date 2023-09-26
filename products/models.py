from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    external_link = models.URLField()
    duration_in_seconds = models.IntegerField()

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
    lessons = models.ManyToManyField(to=Lesson)

    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    ACCESS = 'OPEN'
    NOT_ACCESS = 'CLOSE'
    CHOICES_TO_ACCESS = [
        (ACCESS, 'доступен'),
        (NOT_ACCESS, 'не доступен')
    ]

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    access = models.CharField(max_length=20, choices=CHOICES_TO_ACCESS, default=NOT_ACCESS)

    def __str__(self):
        return f'Доступ ользователя {self.user} к продукту {self.product}'


class LessonView(models.Model):
    IS_WATCHED = 'Просмотрено'
    IS_NOT_WATCHED = 'Не просмотрено'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    view_time_in_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default=IS_NOT_WATCHED, blank=True)
    date_of_last_view = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        lesson_duration = self.lesson.duration_in_seconds
        if (lesson_duration - self.view_time_in_seconds) / lesson_duration <= 0.2:
            self.status = self.IS_WATCHED
        else:
            self.status = self.IS_NOT_WATCHED
        if self.view_time_in_seconds > lesson_duration:
            self.view_time_in_seconds = lesson_duration
        self.date_of_last_view = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Просмотр урока {self.lesson} пользователем {self.user}'
