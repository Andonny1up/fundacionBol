# Generated by Django 4.1.5 on 2023-02-23 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaryapp', '0011_person_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='document',
            field=models.FileField(upload_to='diagnostic/', verbose_name='documento'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='voucher_dona',
            field=models.FileField(upload_to='donations/'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='voucher_expense',
            field=models.FileField(upload_to='expense/', verbose_name='comprobante de gastos'),
        ),
        migrations.AlterField(
            model_name='expensebeneficiary',
            name='voucher_expense',
            field=models.FileField(upload_to='expense/'),
        ),
    ]
