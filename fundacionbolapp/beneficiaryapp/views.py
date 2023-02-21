from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
import datetime
from . import forms, models 


# Create your views here.
# <-- home -->
def home(request):
    return render(request,"beneficiaryapp/home.html")
# <-- home-->

# <-- Beneficiary -->
def create_beneficiary(request):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        c_name =request.POST["c_name"]
        
        person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        if c_name:
            cancer = models.Cancer.objects.get(pk=c_name)
        else:
            cancer = None
            
        bene= models.Beneficiary.objects.create(id_perso=person,id_cancer=cancer)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        type_cancer = models.Cancer.objects.all()
        return render(request,"beneficiaryapp/create_beneficiary.html",{
            'type_cancer':type_cancer,
            'date_now': date_now,
        })


def edit_beneficiary(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    if request.method=="POST":
        beneficiary.id_perso.dni = request.POST["dni"]
        beneficiary.id_perso.name = request.POST["name"]
        beneficiary.id_perso.birthday = request.POST["birthday"]
        beneficiary.id_perso.gender = request.POST["gender"]
        beneficiary.id_perso.phone = request.POST["phone"]
        beneficiary.id_perso.address = request.POST["address"]
        beneficiary.id_perso.save()
        cancer =models.Cancer.objects.get(pk=request.POST["c_name"])
        beneficiary.id_cancer = cancer
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
    

def delete_beneficiary(request,beneficiary_id):
    bene = models.Beneficiary.objects.get(pk=beneficiary_id)
    bene.id_perso.active=False
    bene.id_perso.save()
    return HttpResponseRedirect(reverse("beneficiary:list_beneficiary",))


# <-- Beneficiary -->
# <-- Companion -->
def create_companion(request,beneficiary_id):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        
        bene = models.Beneficiary.objects.get(pk=beneficiary_id)
        person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        companion = models.Companion.objects.create(id_perso=person,id_beneficiary=bene)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/companion/form_create.html",{
        'beneficiary_id': beneficiary_id,
        'date_now':date_now
    })
       

def details_companion(request,companion_id):
    companion = get_object_or_404(models.Companion,pk=companion_id)
    return render(request,"beneficiaryapp/companion/details_companion.html",{
        'companion': companion,
    })


def edit_companion(request,companion_id):
    companion = models.Companion.objects.get(pk=companion_id)
    if request.method=="POST":
        companion.id_perso.dni = request.POST["dni"]
        companion.id_perso.name = request.POST["name"]
        companion.id_perso.birthday = request.POST["birthday"]
        companion.id_perso.gender = request.POST["gender"]
        companion.id_perso.phone = request.POST["phone"]
        companion.id_perso.address = request.POST["address"]
        companion.id_perso.save()
        return HttpResponseRedirect(reverse("beneficiary:details_companion",args=(companion.id,)))
    else:
        text_birthday = companion.id_perso.birthday.__str__()
        return render(request,"beneficiaryapp/companion/edit_companion.html",{
            'companion':companion,
            'text_birthday': text_birthday
        })   


def delete_companion(request,companion_id):
    companion = models.Companion.objects.get(pk=companion_id)
    companion.id_perso.active=False
    companion.id_perso.save()
    return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(companion.id_beneficiary.id,)))
# <-- Companion -->


# <-- Voluntary -->
def create_voluntary(request):
    if request.method=="POST":
        dni = request.POST["dni"]
        name = request.POST["name"]
        birthday = request.POST["birthday"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        job =request.POST["job"]
        
        person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        voluntary = models.Voluntary.objects.create(id_perso=person,job=job)
        return HttpResponseRedirect(reverse("beneficiary:details_voluntary",args=(voluntary.id,)))
    else:
        return render(request,"beneficiaryapp/voluntary/create_voluntary.html",{
        })


def list_voluntary(request):
    voluntaries = models.Voluntary.objects.filter(id_perso__active=True)    
    return render(request,"beneficiaryapp/voluntary/list_voluntary.html",{
        'voluntaries': voluntaries,
    })
    

def details_voluntary(request,voluntary_id):
    voluntary = get_object_or_404(models.Voluntary,pk=voluntary_id)
    return render(request,"beneficiaryapp/voluntary/details_voluntary.html",{
        'voluntary': voluntary,
    })


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
        voluntary.id_perso.save()
        voluntary.save()
        return HttpResponseRedirect(reverse("beneficiary:details_voluntary",args=(voluntary.id,)))
    else:
        text_birthday = voluntary.id_perso.birthday.__str__()
        return render(request,"beneficiaryapp/voluntary/edit_voluntary.html",{
            'voluntary':voluntary,
            'text_birthday':text_birthday,
        })  


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
       
       
def details_donor(request,donor_id):
    donor = get_object_or_404(models.Donor,pk=donor_id)
    donations = donor.donation_set.all()
    return render(request,"beneficiaryapp/donor/details_donor.html",{
        'donor': donor,
        'donations':donations
    })


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


def delete_donor(request,donor_id):
    donor = models.Donor.objects.get(pk=donor_id)
    donor.active=False
    donor.save()
    return HttpResponseRedirect(reverse("beneficiary:list_donor",))

   
def list_donor(request):   
    donors = models.Donor.objects.filter(active=True)
    return render(request,"beneficiaryapp/donor/list_donor.html",{
        'donors': donors,
    })
    
    
def list_donation(request):   
    donations = models.Donation.objects.all()
    return render(request,"beneficiaryapp/donor/list_donation.html",{
        'donations': donations,
    })
# <-- Donor -->


def create_donation(request,donor_id):
    donor = models.Donor.objects.get(pk=donor_id)
    if request.method=="POST":
        amount_donation = request.POST["amount_donation"]
        date_donation = request.POST["date_donation"]
        num_cta = request.POST["num_cta"]
        file = request.FILES["voucher_dona"]
        fs = FileSystemStorage()
        voucher_dona = fs.save(file.name,file)
        
        donation = models.Donation.objects.create(id_donor=donor,amount_donation=amount_donation,date_donation=date_donation,num_cta=num_cta,voucher_dona=voucher_dona)
        return HttpResponseRedirect(reverse("beneficiary:details_donor",args=(donor.id,)))
    else:
        date_now = timezone.now().strftime('%Y-%m-%d')
        return render(request,"beneficiaryapp/donor/create_donation.html",{
        'donor': donor,
        'date_now':date_now,
    })

      
#<-- Diagnostic -->
def list_diagnostic(request,beneficiary_id):
    beneficiary = get_object_or_404(models.Beneficiary,pk=beneficiary_id)
    diagnostics = beneficiary.diagnostic_set.all()
    return render(request,"beneficiaryapp/diagnostic/list_diagnostic.html",{
        'beneficiary': beneficiary,
        'diagnostics':diagnostics,
    })
    
def create_diagnostic(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    if request.method=="POST" and request.FILES["document"]:
        presumptive_name = request.POST["presumptive_name"]
        details = request.POST["details"]
        diagnostic_date = request.POST["diagnostic_date"]
        file = request.FILES["document"]
        fs = FileSystemStorage()
        document = fs.save(file.name,file)
        
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
def create_cancer(request):
    if request.method=="POST":
        c_name = request.POST["c_name"]
        description = request.POST["description"]
        models.Cancer.objects.create(c_name=c_name,description=description)
        return HttpResponseRedirect(reverse("beneficiary:list_cancer"))
    else:
       return render(request,"beneficiaryapp/cancer/create_cancer.html",{
           
    })
       
       
def list_cancer(request):
    cancers = models.Cancer.objects.all()
    return render(request,"beneficiaryapp/cancer/list_cancer.html",{'cancers':cancers})


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
    

def destroy_cancer(request, cancer_id):
    cancer = models.Cancer.objects.get(id=cancer_id)
    cancer.delete()
    return HttpResponseRedirect(reverse("beneficiary:list_cancer"))


#<-- expense -->
def create_expense(request):
    if request.method == "POST":
        expense_amount = request.POST["expense_amount"]
        expense_date = request.POST["expense_date"]
        Description_expense = request.POST["Description_expense"]
        file = request.FILES["voucher_expense"]
        fs = FileSystemStorage()
        voucher_expense = fs.save(file.name,file)
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


def list_expense(request):
    expenses = models.Expense.objects.all()
    return render(request,"beneficiaryapp/expense/list_expense.html",{
        'expenses':expenses
    })
#<-- expense -->


#<-- expense beneficiary-->
def create_expense_beneficiary(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    if request.method == "POST":
        expense_amount = request.POST["expense_amount"]
        expense_date = request.POST["expense_date"]
        motive = request.POST["motive"]
        file = request.FILES["voucher_expense"]
        fs = FileSystemStorage()
        voucher_expense= fs.save(file.name,file)
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
    

def list_expense_beneficiary(request,beneficiary_id):
    beneficiary = models.Beneficiary.objects.get(pk=beneficiary_id)
    expenses = beneficiary.expensebeneficiary_set.all()
    return render(request,"beneficiaryapp/expense/list_expense_beneficiary.html",{
        'beneficiary':beneficiary,
        'expenses':expenses
    })
    

def finalized_expense_beneficiary(request,expense_beneficiary_id):
    expense = models.ExpenseBeneficiary.objects.get(pk=expense_beneficiary_id)
    expense.finalized = True
    expense.save()
    return HttpResponseRedirect(reverse("beneficiary:list_expense_beneficiary",args=(expense.id_beneficiary.id,)))
    
    
#type-expense
def create_type_expense(request):
    if request.method=="POST":
        name = request.POST["name"]
        details = request.POST["details"]
        models.Type_expense.objects.create(name=name,details=details)
        return HttpResponseRedirect(reverse("beneficiary:list_type_expense"))
    else:
       return render(request,"beneficiaryapp/expense/type_expense/create_type_expense.html",{
           
    })
       
       
def list_type_expense(request):
    type_expense = models.Type_expense.objects.all()
    return render(request,"beneficiaryapp/expense/type_expense/list_type_expense.html",{'type_expense':type_expense})


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
    

def destroy_type_expense(request, type_expense_id):
    type_expense = models.Type_expense.objects.get(pk=type_expense_id)
    type_expense.delete()
    return HttpResponseRedirect(reverse("beneficiary:list_type_expense"))


#<--vista cuentas-->
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
def delete_donation(request,donation_id):
    donation = models.Donation.objects.get(pk=donation_id)
    donation.active=False
    donation.save()
    return HttpResponseRedirect(reverse("beneficiary:balance_donations",))


def delete_expense(request,expense_id):
    expense = models.Expense.objects.get(pk=expense_id)
    expense.active=False
    expense.save()
    return HttpResponseRedirect(reverse("beneficiary:balance",))


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