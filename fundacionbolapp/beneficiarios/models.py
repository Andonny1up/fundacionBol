from django.db import models

# Create your models here.
#tablas azules--
class Persona(models.Model):
    dni = models.TextField(max_length=10)
    nombres = models.TextField(max_length=150)
    fecha_nac = models.DateField("fecha de nacimiento")
    genero = models.TextField(max_length=10)
    telefono = models.PositiveIntegerField(default=0)
    direccion = models.TextField(max_length=(250))
    estado_per = models.BooleanField(default=1)

class Donante(models.Model):
    dni = models.TextField(max_length=10)
    nombres = models.TextField(max_length=150)
    tipo = models.TextField(max_length=20)

class Cancer(models.Model):
    nombre_cancer = models.TextField(max_length=200)
    detalles = models.TextField(max_length=350)
    
class TipoGasto(models.Model):
    nombre_gastos = models.TextField(max_length=100)
    detalles_gastos = models.TextField(max_length=350)

#tables celestes--
class Beneficiario(models.Model):
    id_perso = models.ForeignKey(Persona,on_delete=models.CASCADE)
    id_cancer = models.ForeignKey(Cancer,on_delete=models.CASCADE)

class Acompanante(models.Model):
    id_perso = models.ForeignKey(Persona,on_delete=models.CASCADE)
    id_beneficiario = models.ForeignKey(Beneficiario,on_delete=models.CASCADE)
    
class Voluntario(models.Model):
    id_perso = models.ForeignKey(Persona,on_delete=models.CASCADE)
    cargo = models.TextField(max_length=150)
    
class OtrosGastos(models.Model):
    monto_gasto_o = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_gasto_o = models.DateField("fecha otros gastos")
    descripcion_gastos = models.TextField(max_length=350)
    comprobante_gasto_o = models.FileField(upload_to="uploads/")
    id_voluntario = models.ForeignKey(Voluntario,on_delete=models.CASCADE)

# tablas rojas--
class Diagnostico(models.Model):
    nombre_presuntivo = models.TextField(max_length=200)
    detalles = models.TextField(max_length=350)
    fecha_diagnostico = models.DateField("fecha diagnostico")
    documento = models.FileField(upload_to="uploads/")
    id_beneficiario = models.ForeignKey(Beneficiario,on_delete=models.CASCADE)
    
class GastoBeneficiario(models.Model):
    id_beneficiario = models.ForeignKey(Beneficiario,on_delete=models.CASCADE)
    id_tipo_gasto = models.ForeignKey(TipoGasto,on_delete=models.CASCADE)
    monto_gasto = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_gasto = models.DateField("fecha gasto")
    motivo = models.TextField(max_length=150)
    #Aconpanante
    id_voluntario = models.ForeignKey(Voluntario,on_delete=models.CASCADE)
    comprobante_gasto = models.FileField(upload_to="uploads/")
    
class Donacion(models.Model):
    id_donante = models.ForeignKey(Donante,on_delete=models.CASCADE)
    monto_donacion = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_donacion = models.DateField("fecha donacion")
    num_cta = models.TextField(max_length=20)
    #Aconpanante
    comprobante_donar = models.FileField(upload_to="uploads/")
    