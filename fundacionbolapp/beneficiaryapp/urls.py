from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "beneficiary"
urlpatterns = [
    path("",views.home,name="home"),
    path("create/",views.create_beneficiary,name="create_beneficiary"),
    path("list/",views.list_beneficiary,name="list_beneficiary"),
    path("edit/<int:beneficiary_id>",views.edit_beneficiary,name="edit_beneficiary"),
    path("details/<int:beneficiary_id>",views.details,name="details_beneficiary"),
    #ex: deneficiarios/detalles/5/
    #cancers
    path("cancer/create/",views.create_cancer,name="create_cancer"),
    path("cancer/list/",views.list_cancer,name="list_cancer"),
    path("cancer/edit/<int:cancer_id>",views.edit_cancer,name="edit_cancer"),
    path("cancer/delete/<int:cancer_id>",views.destroy_cancer,name="destroy_cancer"),
    
    #companion
    path("companion/create/<int:beneficiary_id>",views.create_companion,name="create_companion"),
    path("companion/details/<int:companion_id>",views.details_companion,name="details_companion"),
    #voluntarios
    path("voluntary/create/",views.create_voluntary,name="create_voluntary"),
    path("voluntary/list/",views.list_voluntary,name="list_voluntary"),
    path("voluntary/details/<int:voluntary_id>",views.details_voluntary,name="details_voluntary"),
    #donations-donor
    path("donor/create/",views.create_donor,name="create_donor"),
    path("donor/details/<int:donor_id>",views.details_donor,name="details_donor"),
    path("donor/list/",views.list_donor,name="list_donor"),
    path("donation/list/",views.list_donation,name="list_donation"),
    path("donor/<int:donor_id>/donation/create/",views.create_donation,name="create_donation"),
    #diagnostic
    path("<int:beneficiary_id>/diagnostic/",views.list_diagnostic,name="list_diagnostic"),
    path("<int:beneficiary_id>/diagnostic/create/",views.create_diagnostic,name="create_diagnostic"),
    #expenses
    path("expense/create/",views.create_expense,name="create_expense"),
    #path("donor/details/<int:donor_id>",views.details_donor,name="details_donor"),
    path("expense/list/",views.list_expense,name="list_expense"),
    #expenses-beneficiary
    path("expense-beneficiary/create/<int:beneficiary_id>",views.create_expense_beneficiary,name="create_expense_beneficiary"),
    #path("donor/details/<int:donor_id>",views.details_donor,name="details_donor"),
    path("expense-beneficiary/list/",views.list_expense_beneficiary,name="list_expense_beneficiary"),
    #type_expense
    path("type-expense/create/",views.create_type_expense,name="create_type_expense"),
    path("type-expense/list/",views.list_type_expense,name="list_type_expense"),
    path("type-expense/edit/<int:type_expense_id>",views.edit_type_expense,name="edit_type_expense"),
    path("type-expense/delete/<int:type_expense_id>",views.destroy_type_expense,name="destroy_type_expense"),
    
    #expense-balance
    path("balance/expense/",views.balance,name="balance"),
    path("balance/donations/",views.balance_donations,name="balance_donations"),
    path("balance/total/",views.balance_total,name="balance_total"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)