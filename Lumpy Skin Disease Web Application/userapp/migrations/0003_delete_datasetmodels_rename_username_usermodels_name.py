# Generated by Django 4.2.7 on 2023-11-27 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_alter_usermodels_username_userfeedbackmodels'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DatasetModels',
        ),
        migrations.RenameField(
            model_name='usermodels',
            old_name='username',
            new_name='name',
        ),
    ]
