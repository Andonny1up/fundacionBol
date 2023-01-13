from django.urls import path
from . import views


app_name = "beneficiarios"
urlpatterns = [
    path("",views.index,name="index"),
    #ex: deneficiarios/detalles/5/
    path("detalles/<int:persona_id>/",views.detallesBeneficiario,name="detallesBeneficiario")
]
