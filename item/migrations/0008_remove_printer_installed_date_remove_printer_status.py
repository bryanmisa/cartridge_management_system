# Generated by Django 4.0.4 on 2022-07-30 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_cartridge_date_disposed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printer',
            name='installed_date',
        ),
        migrations.RemoveField(
            model_name='printer',
            name='status',
        ),
    ]