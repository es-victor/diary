# Generated by Django 4.0.2 on 2022-02-27 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0007_story_title_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='title_length',
            field=models.IntegerField(blank=True),
        ),
    ]
