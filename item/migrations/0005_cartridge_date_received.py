# Generated by Django 4.0.4 on 2022-07-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_cartridgeproductnumber_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartridge',
            name='date_received',
            field=models.DateField(blank=True, null=True),
        ),
    ]
