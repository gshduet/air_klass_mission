from django.db import models


class Master(models.Model):
    name = models.CharField(max_length=10)


class Klass(models.Model):
    master = models.ForeignKey('contentshub.Master', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
