from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class TimeStapedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(TimeStapedModel):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Section(TimeStapedModel):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(TimeStapedModel):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.name


class History(TimeStapedModel):
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    method_name = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
