from django.db import models

# Create your models here.
class Person(models.Model):
    
    dni = models.CharField("dni",max_length=10)
    name = models.CharField("nombre",max_length=150)
    birthday = models.DateField("fecha de nacimiento")
    gender = models.CharField("genero",max_length=10)
    phone = models.CharField("telefono",max_length=10)
    address = models.TextField("direccion",max_length=(250))
    photo = models.ImageField("Foto",upload_to='images/', null=True, blank=True)
    active = models.BooleanField("activo",default=1)
    
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
    id_cancer = models.ForeignKey(Cancer,on_delete=models.SET_NULL, null=True, blank=True)
    origin = models.CharField("Lugar de Origen",max_length=100,null=True, blank=True)
    file_solicitud = models.FileField("solicitud de inclusión",upload_to="solicitud/",null=True, blank=True)
    

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
    active = models.BooleanField("activo", default=1)
    

class Donation(models.Model):
    id_donor = models.ForeignKey(Donor,on_delete=models.CASCADE)
    amount_donation = models.DecimalField("monto de la donacion",max_digits=10,decimal_places=2)
    date_donation = models.DateField("fecha donacion")
    num_cta = models.TextField(max_length=20)
    voucher_dona = models.FileField(upload_to="donations/")
    active = models.BooleanField("activo", default=1)
 
    
#
class Diagnostic(models.Model):
    presumptive_name = models.CharField("nombre presuntivo",max_length=100)
    details = models.TextField("detalles",max_length=350)
    diagnostic_date = models.DateField("fecha diagnostico")
    document = models.FileField("documento",upload_to="diagnostic/")
    id_beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
 
    
# Tablas de Gastos
class Type_expense(models.Model):
    name = models.CharField("nombre gasto",max_length=100)
    details = models.CharField("detalles",max_length=350)
    
    
class ExpenseBeneficiary(models.Model):
    id_beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
    expense_amount = models.DecimalField("monto de gasto",max_digits=10,decimal_places=2)
    expense_date = models.DateField("fecha gasto")
    motive = models.TextField(max_length=150)
    id_companion = models.ForeignKey(Companion,on_delete=models.SET_NULL, null=True, blank=True)
    id_voluntary = models.ForeignKey(Voluntary,on_delete=models.CASCADE)
    voucher_expense = models.FileField(upload_to="expense/")
    finalized = models.BooleanField("finalizado", default=1)
    active = models.BooleanField("activo", default=1)
    
    
class Expense(models.Model):
    expense_amount = models.DecimalField("monto de otros gastos",max_digits=10,decimal_places=2)
    expense_date = models.DateField("fecha otros gastos")
    Description_expense  = models.TextField("Descripcion de gastos",max_length=350)
    voucher_expense  = models.FileField("comprobante de gastos",upload_to="expense/")
    id_voluntary = models.ForeignKey(Voluntary,on_delete=models.CASCADE)
    type_expense = models.ForeignKey(Type_expense,on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField("activo", default=1)