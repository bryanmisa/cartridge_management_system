# Generated by Django 4.0.4 on 2022-05-24 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartridgeproductnumber',
            options={'ordering': ['name']},
        ),
    ]
