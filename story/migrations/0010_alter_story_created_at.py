# Generated by Django 4.0.2 on 2022-02-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0009_story_created_at_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='created_at',
            field=models.DateTimeField(auto_created=True, blank=True),
        ),
    ]
