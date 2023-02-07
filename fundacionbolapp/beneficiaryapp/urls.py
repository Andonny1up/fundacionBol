from django.urls import path
from . import views


app_name = "beneficiary"
urlpatterns = [
    path("",views.home,name="home"),
    path("create/",views.create_beneficiary,name="create_beneficiary"),
    path("list/",views.list_beneficiary,name="list_beneficiary"),
    path("details/<int:beneficiary_id>",views.details,name="details_beneficiary"),
    path("form/",views.form_beneficiary,name="form_beneficiary"),
    #ex: deneficiarios/detalles/5/
    
    #companion
    path("companion/create/<int:beneficiary_id>",views.create_companion,name="create_companion"),
]