# Generated by Django 4.2.1 on 2023-06-06 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customers_bc_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customers',
            options={'verbose_name': 'customer', 'verbose_name_plural': 'customers'},
        ),
    ]