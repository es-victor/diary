# Generated by Django 4.0.2 on 2022-02-28 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0012_remove_tag_created_at_remove_tag_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='created_at_month',
        ),
        migrations.AlterField(
            model_name='story',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
    ]
