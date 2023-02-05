from django.contrib import admin
from .models import Persona,Donante,Cancer,TipoGasto,Beneficiario,Acompanante,Voluntario,OtrosGastos,Diagnostico,GastoBeneficiario,Donacion
# Register your models here.
"""
lista_db =[Persona,
           Donante,
           Cancer,
           TipoGasto,
           Beneficiario,
           Acompanante,
           Voluntario,
           OtrosGastos,
           Diagnostico,
           GastoBeneficiario,
           Donacion]
admin.site.register(lista_db)
"""
class BeneficiarioInline(admin.StackedInline):
    model = Beneficiario
    extra = 1
    autocomplete_fields = ["id_cancer"]


class PersonaAdmin(admin.ModelAdmin):
    inlines = [BeneficiarioInline]
    

class CancerAdmin(admin.ModelAdmin):
    ordering = ["nombre_cancer"]
    search_fields = ["nombre_cancer"]


admin.site.register(Persona,PersonaAdmin)
admin.site.register(Cancer,CancerAdmin)