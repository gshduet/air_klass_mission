# Generated by Django 3.1.14 on 2022-09-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentshub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klass',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='강의 설명'),
        ),
        migrations.AlterField(
            model_name='master',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='강사 설명'),
        ),
    ]
