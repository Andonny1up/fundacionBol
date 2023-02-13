# Generated by Django 4.1.5 on 2023-02-11 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaryapp', '0005_diagnostic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre gasto')),
                ('details', models.CharField(max_length=350, verbose_name='detalles')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseBeneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='monto de gasto')),
                ('expense_date', models.DateField(verbose_name='fecha gasto')),
                ('motive', models.TextField(max_length=150)),
                ('voucher_expense', models.FileField(upload_to='uploads/')),
                ('id_beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaryapp.beneficiary')),
                ('id_type_expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaryapp.type_expense')),
                ('id_voluntary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaryapp.voluntary')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='monto de otros gastos')),
                ('expense_date', models.DateField(verbose_name='fecha otros gastos')),
                ('Description_expense', models.TextField(max_length=350, verbose_name='Descripcion de gastos')),
                ('voucher_expense', models.FileField(upload_to='uploads/', verbose_name='comprobante de gastos')),
                ('id_voluntary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaryapp.voluntary')),
            ],
        ),
    ]
