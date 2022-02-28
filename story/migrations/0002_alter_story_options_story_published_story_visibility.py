# Generated by Django 4.0.2 on 2022-02-27 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'Stories'},
        ),
        migrations.AddField(
            model_name='story',
            name='published',
            field=models.IntegerField(choices=[(0, 'Deleted'), (1, 'Published')], default=1),
        ),
        migrations.AddField(
            model_name='story',
            name='visibility',
            field=models.IntegerField(choices=[(0, 'Public'), (1, 'Private')], default=1),
        ),
    ]
