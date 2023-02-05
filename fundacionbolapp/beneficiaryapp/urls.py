from django.urls import path
from . import views


app_name = "beneficiary"
urlpatterns = [
    path("create/",views.form_create_beneficiary,name="form_create_beneficiary"),
    path("yes/",views.create_beneficiary,name="create_beneficiary"),
    path("form/",views.form_beneficiary,name="form_beneficiary"),
    #ex: deneficiarios/detalles/5/
]