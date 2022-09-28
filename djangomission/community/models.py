from django.db import models


class Question(models.Model):
    contents = models.TextField()


class Answer(models.Model):
    contents = models.TextField()
