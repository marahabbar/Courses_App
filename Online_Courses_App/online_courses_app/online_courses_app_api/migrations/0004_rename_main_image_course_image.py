# Generated by Django 4.1.4 on 2023-02-18 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_courses_app_api', '0003_course_main_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Main_Image',
            new_name='Image',
        ),
    ]
