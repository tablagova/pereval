# Generated by Django 4.1.2 on 2022-10-28 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_coords_table_alter_images_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='users',
            table='pereval_user',
        ),
    ]
