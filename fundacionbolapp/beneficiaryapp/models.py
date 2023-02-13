from django.db import models

# Create your models here.
class Person(models.Model):
    
    dni = models.CharField("dni",max_length=10)
    name = models.CharField("nombre",max_length=150)
    birthday = models.DateField("fecha de nacimiento")
    gender = models.CharField("genero",max_length=10)
    phone = models.CharField("telefono",max_length=10)
    address = models.TextField("direccion",max_length=(250))
    #estado_per = models.BooleanField("Estado persona",default=1)
    
    def __str__(self):
        return self.name
    

class Cancer(models.Model):
    c_name = models.CharField("Tipo de cancer",max_length=200)
    description = models.TextField("descripcion",max_length=350)
    
    class Meta:
        verbose_name = "Cancer"
        verbose_name_plural = "Canceres"
        
    
    def __str__(self):
        return self.c_name
    

class Beneficiary(models.Model):
    id_perso = models.ForeignKey(Person,on_delete=models.CASCADE)
    id_cancer = models.ForeignKey(Cancer,on_delete=models.CASCADE)
    

class Companion(models.Model):
    id_perso = models.ForeignKey(Person,on_delete=models.CASCADE)
    id_beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
    

class Voluntary(models.Model):
    id_perso = models.ForeignKey(Person,on_delete=models.CASCADE)
    job = models.TextField("cargo",max_length=150)
    
    
# Tablas aparte donante donacion    
class Donor(models.Model):
    dni = models.TextField(max_length=10)
    name = models.TextField("nombre",max_length=150)
    type_donor = models.TextField("Tipo de donador",max_length=20)
    

class Donation(models.Model):
    id_donor = models.ForeignKey(Donor,on_delete=models.CASCADE)
    amount_donation = models.DecimalField("monto de la donacion",max_digits=10,decimal_places=2)
    date_donation = models.DateField("fecha donacion")
    num_cta = models.TextField(max_length=20)
    #Aconpanante
    voucher_dona = models.FileField(upload_to="uploads/")
 
    
#
class Diagnostic(models.Model):
    presumptive_name = models.CharField("nombre presuntivo",max_length=100)
    details = models.TextField("detalles",max_length=350)
    diagnostic_date = models.DateField("fecha diagnostico")
    document = models.FileField("documento",upload_to="uploads/")
    id_beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
 
    
# Tablas de Gastos
class Type_expense(models.Model):
    name = models.CharField("nombre gasto",max_length=100)
    details = models.CharField("detalles",max_length=350)
    
    
class ExpenseBeneficiary(models.Model):
    id_beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
    id_type_expense = models.ForeignKey(Type_expense,on_delete=models.CASCADE)
    expense_amount = models.DecimalField("monto de gasto",max_digits=10,decimal_places=2)
    expense_date = models.DateField("fecha gasto")
    motive = models.TextField(max_length=150)
    #Aconpanante
    id_voluntary = models.ForeignKey(Voluntary,on_delete=models.CASCADE)
    voucher_expense = models.FileField(upload_to="uploads/")
    
    
class Expense(models.Model):
    expense_amount = models.DecimalField("monto de otros gastos",max_digits=10,decimal_places=2)
    expense_date = models.DateField("fecha otros gastos")
    Description_expense  = models.TextField("Descripcion de gastos",max_length=350)
    voucher_expense  = models.FileField("comprobante de gastos",upload_to="uploads/")
    id_voluntary = models.ForeignKey(Voluntary,on_delete=models.CASCADE)