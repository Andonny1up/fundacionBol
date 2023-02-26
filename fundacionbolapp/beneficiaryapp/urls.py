from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "beneficiary"
urlpatterns = [
    path("",views.home,name="home"),
    path("beneficiary/create/",views.create_beneficiary,name="create_beneficiary"),
    path("beneficiary/list/",views.list_beneficiary,name="list_beneficiary"),
    path("beneficiary/search/",views.search_beneficiary,name="search_beneficiary"),
    path("beneficiary/edit/<int:beneficiary_id>",views.edit_beneficiary,name="edit_beneficiary"),
    path("beneficiary/details/<int:beneficiary_id>",views.details,name="details_beneficiary"),
    path("beneficiary/delete/<int:beneficiary_id>",views.delete_beneficiary,name="delete_beneficiary"),
    #ex: deneficiarios/detalles/5/
    #cancers
    path("cancer/create/",views.create_cancer,name="create_cancer"),
    path("cancer/list/",views.list_cancer,name="list_cancer"),
    path("cancer/edit/<int:cancer_id>",views.edit_cancer,name="edit_cancer"),
    path("cancer/delete/<int:cancer_id>",views.destroy_cancer,name="destroy_cancer"),
    
    #companion
    path("companion/create/<int:beneficiary_id>",views.create_companion,name="create_companion"),
    path("companion/details/<int:companion_id>",views.details_companion,name="details_companion"),
    path("companion/edit/<int:companion_id>",views.edit_companion,name="edit_companion"),
    path("companion/delete/<int:companion_id>",views.delete_companion,name="delete_companion"),
    #voluntarios
    path("voluntary/create/",views.create_voluntary,name="create_voluntary"),
    path("voluntary/list/",views.list_voluntary,name="list_voluntary"),
    path("voluntary/details/<int:voluntary_id>",views.details_voluntary,name="details_voluntary"),
    path("voluntary/edit/<int:voluntary_id>",views.edit_voluntary,name="edit_voluntary"),
    path("voluntary/delete/<int:voluntary_id>",views.delete_voluntary,name="delete_voluntary"),
    #donations-donor
    path("donor/create/",views.create_donor,name="create_donor"),
    path("donor/details/<int:donor_id>",views.details_donor,name="details_donor"),
    path("donor/edit/<int:donor_id>",views.edit_donor,name="edit_donor"),
    path("donor/delete/<int:donor_id>",views.delete_donor,name="delete_donor"),
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
    path("expense-beneficiary/list/<int:beneficiary_id>",views.list_expense_beneficiary,name="list_expense_beneficiary"),
    path("expense-beneficiary/finalized/<int:expense_beneficiary_id>",views.finalized_expense_beneficiary,name="finalized_expense_beneficiary"),
    #type_expense
    path("type-expense/create/",views.create_type_expense,name="create_type_expense"),
    path("type-expense/list/",views.list_type_expense,name="list_type_expense"),
    path("type-expense/edit/<int:type_expense_id>",views.edit_type_expense,name="edit_type_expense"),
    path("type-expense/delete/<int:type_expense_id>",views.destroy_type_expense,name="destroy_type_expense"),
    
    #expense-balance
    path("balance/expense/",views.balance,name="balance"),
    path("balance/donations/",views.balance_donations,name="balance_donations"),
    path("balance/total/",views.balance_total,name="balance_total"),
    
    #delete-balance
    path("delete/donation/<donation_id>",views.delete_donation,name="delete_donation"),
    path("delete/expense/<expense_id>",views.delete_expense,name="delete_expense"),
    path("delete/expense-beneficiary/<expense_id>",views.delete_expense_beneficiary,name="delete_expense_beneficiary"),
    
    #deleted
    path("deleted/",views.deleted,name="deleted"),
     
    #graphics
    path("graphics/",views.graphic_type_cancer,name="graphic_type_cancer"),
    
    #login
    path("login/", auth_views.LoginView.as_view(),name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth import views as auth_views
