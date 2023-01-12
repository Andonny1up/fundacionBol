from django.contrib import admin
from .models import Persona,Beneficiario,Diagnostico 
# Register your models here.
lista_db =[Persona,Beneficiario,Diagnostico]
admin.site.register(lista_db)