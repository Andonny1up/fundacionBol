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