# Generated by Django 4.1.5 on 2023-02-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaryapp', '0010_expensebeneficiary_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Foto'),
        ),
    ]