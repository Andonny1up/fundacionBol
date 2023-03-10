# Generated by Django 4.1.5 on 2023-02-09 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaryapp', '0004_voluntary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presumptive_name', models.CharField(max_length=100, verbose_name='nombre presuntivo')),
                ('details', models.TextField(max_length=350, verbose_name='detalles')),
                ('diagnostic_date', models.DateField(verbose_name='fecha diagnostico')),
                ('document', models.FileField(upload_to='uploads/', verbose_name='documento')),
                ('id_beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaryapp.beneficiary')),
            ],
        ),
    ]
