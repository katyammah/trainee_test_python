# Generated by Django 4.2.5 on 2023-09-24 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_owner_lessonview'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonview',
            name='status',
            field=models.CharField(default='Не просмотрено', max_length=30),
        ),
    ]