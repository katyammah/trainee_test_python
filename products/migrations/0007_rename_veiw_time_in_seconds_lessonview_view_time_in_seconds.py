# Generated by Django 4.2.5 on 2023-09-25 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_lessonview_veiw_time_in_seconds_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonview',
            old_name='veiw_time_in_seconds',
            new_name='view_time_in_seconds',
        ),
    ]
