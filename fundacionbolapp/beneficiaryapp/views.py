from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
import datetime
from . import forms, models
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import View
from django.contrib.auth import views as auth_views
from openpyxl import Workbook

def user_is_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(user_is_not_authenticated, login_url='beneficiary:home')
def my_login_view(request):
    # Usa el `LoginView` de Django para renderizar la vista de inicio de sesión
    return auth_views.LoginView.as_view()(request)   
    
    
class ExportToExcel(View):
    def get(self, request):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="datos.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos"
        ws.append(['CI','Nombre', 'Fecha de Nacimiento','Genero','Celular','Lugar Origen','Dirreccion','Diagnostico'])
        for item in models.Beneficiary.objects.all().values_list('id_perso__dni', 'id_perso__name', 'id_perso__birthday','id_perso__gender','id_perso__phone','origin','id_perso__address','id_cancer__c_name'):
        #ws.append(['CI','Nombre'])
        #for item in models.Beneficiary.objects.all().values_list('id_perso__dni', 'id_perso__name'):    
            ws.append(item)
        wb.save(response)
        return response


@login_required
def register(request):
    if request.user.can_register:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('beneficiary:home')
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    else:
        return HttpResponse("You are not authorized to register new users.")


# Create your views here.
# <-- home -->
@login_required
def home(request):
    return render(request,"beneficiaryapp/home.html",{})
# <-- home-->

# <-- Beneficiary -->
@login_required
def create_beneficiary(request):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        c_name =request.POST["c_name"]
        origin = request.POST["origin"]
        file_solicitud = request.FILES["file_solicitud"]

        if request.FILES.get('photo'):
            photo= request.FILES["photo"]
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address,photo=photo)
        else:
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        
        if c_name:
            cancer = models.Cancer.objects.get(pk=c_name)
        else:
            cancer = None
            
        bene= models.Beneficiary.objects.create(id_perso=person,id_cancer=cancer,origin=origin,file_solicitud=file_solicitud)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        type_cancer = models.Cancer.objects.all()
        return render(request,"beneficiaryapp/create_beneficiary.html",{
            'type_cancer':type_cancer,
            'date_now': date_now,
        })


@login_required
def edit_beneficiary(request,beneficiary_id):
    beneficiary = get_object_or_404(models.Beneficiary,pk=beneficiary_id)
    if request.method=="POST":
        beneficiary.id_perso.dni = request.POST["dni"]
        beneficiary.id_perso.name = request.POST["name"]
        beneficiary.id_perso.birthday = request.POST["birthday"]
        beneficiary.id_perso.gender = request.POST["gender"]
        beneficiary.id_perso.phone = request.POST["phone"]
        beneficiary.id_perso.address = request.POST["address"]
        if request.FILES.get('photo'):
            beneficiary.id_perso.photo = request.FILES['photo']
            
        beneficiary.id_perso.save()
            
        cancer =models.Cancer.objects.get(pk=request.POST["c_name"])
        origin = request.POST["origin"]
        beneficiary.id_cancer = cancer
        beneficiary.origin = origin
        beneficiary.save()
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(beneficiary.id,)))
    else:
        cancer = models.Cancer.objects.all()
        text_birthday = beneficiary.id_perso.birthday.__str__()
        return render(request,"beneficiaryapp/edit_beneficiary.html",{
            'beneficiary':beneficiary,
            'type_cancer':cancer,
            'text_birthday': text_birthday
        })
    

@login_required
def list_beneficiary(request):
    if request.method=="POST" and request.POST["c_name"]!="Todo":
        c_name = request.POST["c_name"]
        beneficiaries = models.Beneficiary.objects.filter(id_cancer=c_name)
    else:    
        beneficiaries = models.Beneficiary.objects.filter(id_perso__active=True)
        
    cancer = models.Cancer.objects.all()
    return render(request,"beneficiaryapp/list_beneficiary.html",{
        'beneficiaries': beneficiaries,
        'type_cancer': cancer,
    })
    

@login_required
def search_beneficiary(request):
    
    if request.GET["search_text"]:
        f_filter = request.GET["f_filter"]
        search_text = request.GET["search_text"]
        
        if f_filter == "dni":
            beneficiaries = models.Beneficiary.objects.filter(id_perso__active=True,id_perso__dni__icontains=search_text)
            #article = Article.objects.filter(name__icontains=product)
            dni = True
        else:
            beneficiaries = models.Beneficiary.objects.filter(id_perso__active=True,id_perso__name__icontains=search_text)
            dni = False
            
        return render(request,"beneficiaryapp/search_beneficiary.html",{
                'beneficiaries': beneficiaries,
                'search_text':search_text,
                'f_filter':dni,
                
            })
    
    return HttpResponseRedirect(reverse("beneficiary:list_beneficiary",))
    

@login_required
def details(request,beneficiary_id):
    #bene = models.Beneficiary.objects.get(pk=beneficiary_id)
    bene = get_object_or_404(models.Beneficiary,pk=beneficiary_id)
    companions = bene.companion_set.filter(id_perso__active=True)
    expense_pendien = bene.expensebeneficiary_set.filter(finalized=False)
    return render(request,"beneficiaryapp/details_beneficiary.html",{
        'beneficiary': bene,
        'companions': companions,
        'expense_pendien':expense_pendien,
    })
    

@login_required
def delete_beneficiary(request,beneficiary_id):
    bene = models.Beneficiary.objects.get(pk=beneficiary_id)
    bene.id_perso.active=False
    bene.id_perso.save()
    return HttpResponseRedirect(reverse("beneficiary:list_beneficiary",))


# <-- Beneficiary -->
# <-- Companion -->
@login_required
def create_companion(request,beneficiary_id):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        if request.FILES.get('photo'):
            photo= request.FILES["photo"]
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address,photo=photo)
        else:
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        
        bene = models.Beneficiary.objects.get(pk=beneficiary_id)
        
        companion = models.Companion.objects.create(id_perso=person,id_beneficiary=bene)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/companion/form_create.html",{
        'beneficiary_id': beneficiary_id,
        'date_now':date_now
    })
       

@login_required
def details_companion(request,companion_id):
    companion = get_object_or_404(models.Companion,pk=companion_id)
    return render(request,"beneficiaryapp/companion/details_companion.html",{
        'companion': companion,
    })


@login_required
def edit_companion(request,companion_id):
    companion = models.Companion.objects.get(pk=companion_id)
    if request.method=="POST":
        companion.id_perso.dni = request.POST["dni"]
        companion.id_perso.name = request.POST["name"]
        companion.id_perso.birthday = request.POST["birthday"]
        companion.id_perso.gender = request.POST["gender"]
        companion.id_perso.phone = request.POST["phone"]
        companion.id_perso.address = request.POST["address"]
        if request.FILES.get('photo'):
            companion.id_perso.photo = request.FILES['photo']
            
        companion.id_perso.save()
        return HttpResponseRedirect(reverse("beneficiary:details_companion",args=(companion.id,)))
    else:
        text_birthday = companion.id_perso.birthday.__str__()
        return render(request,"beneficiaryapp/companion/edit_companion.html",{
            'companion':companion,
            'text_birthday': text_birthday
        })   


@login_required
def delete_companion(request,companion_id):
    companion = models.Companion.objects.get(pk=companion_id)
    companion.id_perso.active=False
    companion.id_perso.save()
    return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(companion.id_beneficiary.id,)))
# <-- Companion -->


# <-- Voluntary -->
@login_required
def create_voluntary(request):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        job =request.POST["job"]
        
        if request.FILES.get('photo'):
            photo= request.FILES["photo"]
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address, photo=photo)
        else:
            person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        
        voluntary = models.Voluntary.objects.create(id_perso=person,job=job)
        return HttpResponseRedirect(reverse("beneficiary:details_voluntary",args=(voluntary.id,)))
    else:
        return render(request,"beneficiaryapp/voluntary/create_voluntary.html",{
        })


@login_required
def list_voluntary(request):
    voluntaries = models.Voluntary.objects.filter(id_perso__active=True)    
    return render(request,"beneficiaryapp/voluntary/list_voluntary.html",{
        'voluntaries': voluntaries,
    })
    

@login_required
def details_voluntary(request,voluntary_id):
    voluntary = get_object_or_404(models.Voluntary,pk=voluntary_id)
    return render(request,"beneficiaryapp/voluntary/details_voluntary.html",{
        'voluntary': voluntary,
    })


@login_required
def edit_voluntary(request,voluntary_id):
    voluntary = models.Voluntary.objects.get(pk=voluntary_id)
    if request.method=="POST":
        voluntary.id_perso.dni = request.POST["dni"]
        voluntary.id_perso.name = request.POST["name"]
        voluntary.id_perso.birthday = request.POST["birthday"]
        voluntary.id_perso.gender = request.POST["gender"]
        voluntary.id_perso.phone = request.POST["phone"]
        voluntary.id_perso.address = request.POST["address"]
        voluntary.job =request.POST["job"]
        if request.FILES.get('photo'):
            voluntary.id_perso.photo = request.FILES['photo']
            
        voluntary.id_perso.save()
        voluntary.save()
        return HttpResponseRedirect(reverse("beneficiary:details_voluntary",args=(voluntary.id,)))
    else:
        text_birthday = voluntary.id_perso.birthday.__str__()
        return render(request,"beneficiaryapp/voluntary/edit_voluntary.html",{
            'voluntary':voluntary,
            'text_birthday':text_birthday,
        })  


@login_required
def delete_voluntary(request,voluntary_id):
    voluntary = models.Voluntary.objects.get(pk=voluntary_id)
    if voluntary.id_perso.active:
        voluntary.id_perso.active=False
        voluntary.id_perso.save()
        return HttpResponseRedirect(reverse("beneficiary:list_voluntary",))
    else:
        voluntary.id_perso.active=True
        voluntary.id_perso.save()
        
    return HttpResponseRedirect(reverse("beneficiary:list_voluntary",))
# <-- Voluntary -->


# <-- Donor -->
@login_required
def create_donor(request):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        type_donor = request.POST["type_donor"]
        
        donor = models.Donor.objects.create(dni = dni,name = name,type_donor = type_donor)
        return HttpResponseRedirect(reverse("beneficiary:details_donor",args=(donor.id,)))
    else:
       return render(request,"beneficiaryapp/donor/create_donor.html",{
        
    })
       

@login_required      
def details_donor(request,donor_id):
    donor = get_object_or_404(models.Donor,pk=donor_id)
    donations = donor.donation_set.all().order_by('-date_donation')
    return render(request,"beneficiaryapp/donor/details_donor.html",{
        'donor': donor,
        'donations':donations
    })


@login_required
def edit_donor(request,donor_id):
    donor = models.Donor.objects.get(pk=donor_id)
    if request.method=="POST":
        donor.dni = request.POST["dni"]
        donor.name = request.POST["name"]
        donor.type_donor = request.POST["type_donor"]
        donor.save()
        return HttpResponseRedirect(reverse("beneficiary:details_donor",args=(donor.id,)))
    else:
        return render(request,"beneficiaryapp/donor/edit_donor.html",{
            'donor':donor,
        })  


@login_required
def delete_donor(request,donor_id):
    donor = models.Donor.objects.get(pk=donor_id)
    donor.active=False
    donor.save()
    return HttpResponseRedirect(reverse("beneficiary:list_donor",))


@login_required 
def list_donor(request):   
    donors = models.Donor.objects.filter(active=True)
    return render(request,"beneficiaryapp/donor/list_donor.html",{
        'donors': donors,
    })
    

@login_required 
def list_donation(request):   
    donations = models.Donation.objects.all()
    return render(request,"beneficiaryapp/donor/list_donation.html",{
        'donations': donations,
    })
# <-- Donor -->


@login_required
def create_donation(request,donor_id):
    donor = models.Donor.objects.get(pk=donor_id)
    if request.method=="POST":
        amount_donation = request.POST["amount_donation"]
        date_donation = request.POST["date_donation"]
        num_cta = request.POST["num_cta"]
        voucher_dona = request.FILES["voucher_dona"]
        
        donation = models.Donation.objects.create(id_donor=donor,amount_donation=amount_donation,date_donation=date_donation,num_cta=num_cta,voucher_dona=voucher_dona)
        return HttpResponseRedirect(reverse("beneficiary:details_donor",args=(donor.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/donor/create_donation.html",{
        'donor': donor,
        'date_now':date_now,
    })

      
#<-- Diagnostic -->
@login_required
def list_diagnostic(request,beneficiary_id):
    beneficiary = get_object_or_404(models.Beneficiary,pk=beneficiary_id)
    diagnostics = beneficiary.diagnostic_set.all().order_by("-diagnostic_date")
    return render(request,"beneficiaryapp/diagnostic/list_diagnostic.html",{
        'beneficiary': beneficiary,
        'diagnostics':diagnostics,
    })


@login_required    
def create_diagnostic(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    if request.method=="POST" and request.FILES["document"]:
        presumptive_name = request.POST["presumptive_name"]
        details = request.POST["details"]
        diagnostic_date = request.POST["diagnostic_date"]
        document = request.FILES["document"]
        
        diagnostic = models.Diagnostic.objects.create(presumptive_name=presumptive_name,details=details,diagnostic_date=diagnostic_date,document=document,id_beneficiary = beneficiary)
        return HttpResponseRedirect(reverse("beneficiary:list_diagnostic",args=(beneficiary.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/diagnostic/create_diagnostic.html",{
        'beneficiary': beneficiary,
        'date_now':date_now,
    })
#<-- Diagnostic -->


#<-- Cancer -->
@login_required
def create_cancer(request):
    if request.method=="POST":
        c_name = request.POST["c_name"]
        description = request.POST["description"]
        models.Cancer.objects.create(c_name=c_name,description=description)
        return HttpResponseRedirect(reverse("beneficiary:list_cancer"))
    else:
       return render(request,"beneficiaryapp/cancer/create_cancer.html",{
           
    })
       

@login_required    
def list_cancer(request):
    cancers = models.Cancer.objects.all()
    return render(request,"beneficiaryapp/cancer/list_cancer.html",{'cancers':cancers})


@login_required
def edit_cancer(request,cancer_id):
    cancer = models.Cancer.objects.get(pk=cancer_id)
    if request.method=="POST":
        cancer.c_name = request.POST["c_name"]
        cancer.description = request.POST["description"]
        cancer.save()
        return HttpResponseRedirect(reverse("beneficiary:list_cancer"))
    else:
        return render(request,"beneficiaryapp/cancer/edit_cancer.html",{
            'cancer':cancer
        })
    

@login_required
def destroy_cancer(request, cancer_id):
    cancer = models.Cancer.objects.get(id=cancer_id)
    cancer.delete()
    return HttpResponseRedirect(reverse("beneficiary:list_cancer"))


#<-- expense -->
@login_required
def create_expense(request):
    if request.method == "POST":
        expense_amount = request.POST["expense_amount"]
        expense_date = request.POST["expense_date"]
        Description_expense = request.POST["Description_expense"]
        voucher_expense = request.FILES["voucher_expense"]
        id_voluntary = request.POST["id_voluntary"]
        id_type_expense = request.POST["type_expense"]
        
        if id_type_expense:
            type_expense = models.Type_expense.objects.get(pk=id_type_expense)
        else:
            type_expense = None
            
        voluntary = models.Voluntary.objects.get(pk=id_voluntary)
        expense = models.Expense.objects.create(expense_amount=expense_amount,expense_date=expense_date,Description_expense=Description_expense,voucher_expense=voucher_expense,type_expense=type_expense,id_voluntary=voluntary)
        return HttpResponseRedirect(reverse("beneficiary:list_expense"))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        voluntaries = models.Voluntary.objects.filter(job='Administrador del sistema',id_perso__active = True)
        type_expense = models.Type_expense.objects.all()
        return render(request,"beneficiaryapp/expense/create_expense.html",{
            'voluntaries':voluntaries,
            'date_now':date_now,
            'type_expense':type_expense,
        })


@login_required
def list_expense(request):
    expenses = models.Expense.objects.all().order_by('-expense_date')
    return render(request,"beneficiaryapp/expense/list_expense.html",{
        'expenses':expenses
    })
#<-- expense -->


#<-- expense beneficiary-->
@login_required
def create_expense_beneficiary(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    if request.method == "POST":
        expense_amount = request.POST["expense_amount"]
        expense_date = request.POST["expense_date"]
        motive = request.POST["motive"]
        voucher_expense= request.FILES["voucher_expense"]
        #id_type_expense = request.POST["id_type_expense"]
        id_companion = request.POST["id_companion"]
        id_voluntary = request.POST["id_voluntary"]
        finalized = request.POST["finalized"]
        voluntary = models.Voluntary.objects.get(pk=id_voluntary)
        if id_companion:
            companion = models.Companion.objects.get(pk=id_companion)
        else:
            companion = None
        expense = models.ExpenseBeneficiary.objects.create(
            id_beneficiary= beneficiary,
            expense_amount = expense_amount,
            expense_date = expense_date,
            motive = motive,
            voucher_expense = voucher_expense,
            id_companion = companion,
            id_voluntary = voluntary,
            finalized = finalized,
        )
        return HttpResponseRedirect(reverse("beneficiary:list_expense_beneficiary",args=(beneficiary.id,)))
    else:
        voluntaries = models.Voluntary.objects.filter(job='Administrador del sistema',id_perso__active = True)
        companions = beneficiary.companion_set.all()
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/expense/create_expense_beneficiary.html",{
            'voluntaries':voluntaries,
            'companions':companions,
            'beneficiary':beneficiary,
            'date_now': date_now,
        })
    

@login_required
def list_expense_beneficiary(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    expenses = beneficiary.expensebeneficiary_set.all().order_by('-expense_date')
    return render(request,"beneficiaryapp/expense/list_expense_beneficiary.html",{
        'beneficiary':beneficiary,
        'expenses':expenses
    })
    

@login_required
def finalized_expense_beneficiary(request,expense_beneficiary_id):
    expense = models.ExpenseBeneficiary.objects.get(pk=expense_beneficiary_id)
    expense.finalized = True
    expense.save()
    return HttpResponseRedirect(reverse("beneficiary:list_expense_beneficiary",args=(expense.id_beneficiary.id,)))
    
    
#type-expense
@login_required
def create_type_expense(request):
    if request.method=="POST":
        name = request.POST["name"]
        details = request.POST["details"]
        models.Type_expense.objects.create(name=name,details=details)
        return HttpResponseRedirect(reverse("beneficiary:list_type_expense"))
    else:
       return render(request,"beneficiaryapp/expense/type_expense/create_type_expense.html",{
           
    })
       

@login_required      
def list_type_expense(request):
    type_expense = models.Type_expense.objects.all()
    return render(request,"beneficiaryapp/expense/type_expense/list_type_expense.html",{'type_expense':type_expense})


@login_required
def edit_type_expense(request,type_expense_id):
    type_expense = models.Type_expense.objects.get(pk=type_expense_id)
    if request.method=="POST":
        type_expense.name = request.POST["name"]
        type_expense.details = request.POST["details"]
        type_expense.save()
        return HttpResponseRedirect(reverse("beneficiary:list_type_expense"))
    else:
        return render(request,"beneficiaryapp/expense/type_expense/edit_type_expense.html",{
            'type_expense':type_expense
        })
    

@login_required
def destroy_type_expense(request, type_expense_id):
    type_expense = models.Type_expense.objects.get(pk=type_expense_id)
    type_expense.delete()
    return HttpResponseRedirect(reverse("beneficiary:list_type_expense"))


#<--vista cuentas-->
@login_required
def balance(request): #expenses
    if request.method=="POST":
        date_init= request.POST["date_init"]
        date_limit= request.POST["date_limit"]
    else:
        date_init = (timezone.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        date_limit = timezone.now().strftime('%Y-%m-%d')
        
    expenses = models.Expense.objects.filter(expense_date__gte=date_init,expense_date__lte=date_limit).order_by('-expense_date')
    expenses_beneficiary = models.ExpenseBeneficiary.objects.filter(expense_date__gte=date_init,expense_date__lte=date_limit).order_by('-expense_date')
    
    expenses_active = expenses.filter(active=True)
    expenses_active_beneficiary = expenses_beneficiary.filter(active=True)
    
    total_num_expense = expenses.count() + expenses_beneficiary.count()
    t_expense_gasto = expenses_active.aggregate(total=Sum('expense_amount',default=0))['total']
    t_expense_gasto_beneficiary = expenses_active_beneficiary.aggregate(total=Sum('expense_amount',default=0))['total']
    total_expense = t_expense_gasto + t_expense_gasto_beneficiary
    
    
    return render(request,"beneficiaryapp/balance/balance_expense.html",{
            'expenses':expenses,
            'date_init':date_init,
            'date_limit':date_limit,
            'total_num_expense':total_num_expense,
            't_expense_gasto':t_expense_gasto,
            't_expense_gasto_beneficiary':t_expense_gasto_beneficiary,
            'total_expense': total_expense,
            'expenses_beneficiary':expenses_beneficiary,
        })


@login_required   
def balance_donations(request):
    if request.method=="POST":
        date_init= request.POST["date_init"]
        date_limit= request.POST["date_limit"]
    else:
        date_init = (timezone.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        date_limit = timezone.now().strftime('%Y-%m-%d')
        
    donations = models.Donation.objects.filter(date_donation__gte=date_init,date_donation__lte=date_limit).order_by('-date_donation')
    donations_valide = donations.filter(active=True)
    total_num_donations = donations.count()
    total_donations = donations_valide.aggregate(total=Sum('amount_donation',default=0))['total']
    
    return render(request,"beneficiaryapp/balance/balance_donations.html",{
            'donations':donations,
            'date_init':date_init,
            'date_limit':date_limit,
            'total_num_donations':total_num_donations,
            'total_donations': total_donations,
        })
    

@login_required
def balance_total(request):
    if request.method=="POST":
        date_init= request.POST["date_init"]
        date_limit= request.POST["date_limit"]
    else:
        date_init = (timezone.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        date_limit = timezone.now().strftime('%Y-%m-%d')
        
    donations = models.Donation.objects.filter(date_donation__gte=date_init,date_donation__lte=date_limit)
    donations_valide = donations.filter(active=True)
    total_donations = donations_valide.aggregate(total=Sum('amount_donation',default=0))['total']
    
    expenses = models.Expense.objects.filter(expense_date__gte=date_init,expense_date__lte=date_limit)
    expenses_beneficiary = models.ExpenseBeneficiary.objects.filter(expense_date__gte=date_init,expense_date__lte=date_limit)
    
    expenses_active = expenses.filter(active=True)
    expenses_active_beneficiary = expenses_beneficiary.filter(active=True)
    
    
    t_expense_gasto = expenses_active.aggregate(total=Sum('expense_amount',default=0))['total']
    t_expense_gasto_beneficiary = expenses_active_beneficiary.aggregate(total=Sum('expense_amount',default=0))['total']
    total_expense = t_expense_gasto + t_expense_gasto_beneficiary
    
    balance = total_donations - total_expense
    #grafico
    
    return render(request,"beneficiaryapp/balance/balance_total.html",{
            'date_init':date_init,
            'date_limit':date_limit,
            
            'donations':donations,
            'total_donations': total_donations,
            
            'expenses':expenses,
            't_expense_gasto':t_expense_gasto,
            't_expense_gasto_beneficiary':t_expense_gasto_beneficiary,
            'total_expense': total_expense,
            'expenses_beneficiary':expenses_beneficiary,
            'total_balance': balance
        })


#<-- delete balance -->
@login_required
def delete_donation(request,donation_id):
    donation = models.Donation.objects.get(pk=donation_id)
    donation.active=False
    donation.save()
    return HttpResponseRedirect(reverse("beneficiary:balance_donations",))


@login_required
def delete_expense(request,expense_id):
    expense = models.Expense.objects.get(pk=expense_id)
    expense.active=False
    expense.save()
    return HttpResponseRedirect(reverse("beneficiary:balance",))


@login_required
def delete_expense_beneficiary(request,expense_id):#expense beneficiary
    expense = models.ExpenseBeneficiary.objects.get(pk=expense_id)
    expense.active=False
    expense.save()
    return HttpResponseRedirect(reverse("beneficiary:balance",))


def deleted(request):
    beneficiary = models.Beneficiary.objects.filter(id_perso__active=False)
    companion = models.Companion.objects.filter(id_perso__active=False)
    voluntary = models.Voluntary.objects.filter(id_perso__active=False)
    donor = models.Donor.objects.filter(active=False)
    
    return render(request,'beneficiaryapp/deleted/list_deleted.html',{
        'beneficiaries':beneficiary,
        'companions':companion,
        'voluntaries': voluntary,
        'donors': donor,
    })
    

#<----------------------- GRAPHICS ------------------>
def graphic_type_cancer(request):
    data = []
    first = True
    type_cancer = models.Cancer.objects.all()
    total_beneficiary = models.Beneficiary.objects.filter(id_perso__active=True).count()
    for cancer in type_cancer:
        beneficiary_list= cancer.beneficiary_set.filter(id_perso__active=True)
        number_beneficiary_part = beneficiary_list.count()
        porc = (number_beneficiary_part * 100)/total_beneficiary
        if first:
            dic = {
            'name':cancer.c_name,
            'y': porc,
        }
        else:
            dic = {
            'name':cancer.c_name,
            'y': porc,
            'sliced': 'true',
            'selected': 'true'
        }
        data.append(dic)
        first=False
        
    return render(request,'beneficiaryapp/graphics/type_cancer.html',{
        'data_type_cancer': data,
    })
    

def view_404(request, exception):
    return HttpResponseNotFound(render(request, 'beneficiaryapp/404.html'))


def view_404_acces(request):
    return render(request, 'beneficiaryapp/404.html')