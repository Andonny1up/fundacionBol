from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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
        cancer = models.Cancer.objects.get(pk=c_name)
        bene= models.Beneficiary.objects.create(id_perso=person,id_cancer=cancer)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
        type_cancer = models.Cancer.objects.all()
        return render(request,"beneficiaryapp/create_beneficiary.html",{
            'type_cancer':type_cancer
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
        beneficiaries = models.Beneficiary.objects.all()
        
    cancer = models.Cancer.objects.all()
    return render(request,"beneficiaryapp/list_beneficiary.html",{
        'beneficiaries': beneficiaries,
        'type_cancer': cancer,
    })
    

def details(request,beneficiary_id):
    #bene = models.Beneficiary.objects.get(pk=beneficiary_id)
    bene = get_object_or_404(models.Beneficiary,pk=beneficiary_id)
    companions = models.Companion.objects.filter(id_beneficiary=beneficiary_id)
    return render(request,"beneficiaryapp/details_beneficiary.html",{
        'beneficiary': bene,
        'companions': companions,
    })
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
       return render(request,"beneficiaryapp/companion/form_create.html",{
        'beneficiary_id': beneficiary_id
    })
       

def details_companion(request,companion_id):
    companion = get_object_or_404(models.Companion,pk=companion_id)
    return render(request,"beneficiaryapp/companion/details_companion.html",{
        'companion': companion,
    })
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
    voluntaries = models.Voluntary.objects.all()    
    return render(request,"beneficiaryapp/voluntary/list_voluntary.html",{
        'voluntaries': voluntaries,
    })
    

def details_voluntary(request,voluntary_id):
    voluntary = get_object_or_404(models.Voluntary,pk=voluntary_id)
    return render(request,"beneficiaryapp/voluntary/details_voluntary.html",{
        'voluntary': voluntary,
    })
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
    
    
def list_donor(request):   
    donors = models.Donor.objects.all()
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
        voucher_dona = request.POST["voucher_dona"]
        
        donation = models.Donation.objects.create(id_donor=donor,amount_donation=amount_donation,date_donation=date_donation,num_cta=num_cta,voucher_dona=voucher_dona)
        return HttpResponseRedirect(reverse("beneficiary:details_donor",args=(donor.id,)))
    else:
       return render(request,"beneficiaryapp/donor/create_donation.html",{
        'donor': donor
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
    if request.method=="POST":
        presumptive_name = request.POST["presumptive_name"]
        details = request.POST["details"]
        diagnostic_date = request.POST["diagnostic_date"]
        document = request.POST["document"]
        
        diagnostic = models.Diagnostic.objects.create(presumptive_name=presumptive_name,details=details,diagnostic_date=diagnostic_date,document=document,id_beneficiary = beneficiary)
        return HttpResponseRedirect(reverse("beneficiary:list_diagnostic",args=(beneficiary.id,)))
    else:
       return render(request,"beneficiaryapp/diagnostic/create_diagnostic.html",{
        'beneficiary': beneficiary
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
        voucher_expense= request.POST["voucher_expense"]
        id_voluntary = request.POST["id_voluntary"]
        
        voluntary = models.Voluntary.objects.get(pk=id_voluntary)
        expense = models.Expense.objects.create(expense_amount=expense_amount,expense_date=expense_date,Description_expense=Description_expense,voucher_expense=voucher_expense,id_voluntary=voluntary)
        return HttpResponseRedirect(reverse("beneficiary:list_expense"))
    else:
        voluntaries = models.Voluntary.objects.all()
        return render(request,"beneficiaryapp/expense/create_expense.html",{
            'voluntaries':voluntaries
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
        voucher_expense= request.POST["voucher_expense"]
        
        id_type_expense = request.POST["id_type_expense"]
        id_voluntary = request.POST["id_voluntary"]
        
        voluntary = models.Voluntary.objects.get(pk=id_voluntary)
        type_expense = models.Type_expense.objects.get(pk=id_type_expense)
        expense = models.ExpenseBeneficiary.objects.create(
            id_beneficiary= beneficiary,
            id_type_expense = type_expense,
            expense_amount = expense_amount,
            expense_date = expense_date,
            motive = motive,
            voucher_expense = voucher_expense,
            id_voluntary = voluntary
        )
        return HttpResponseRedirect(reverse("beneficiary:list_expense_beneficiary"))
    else:
        voluntaries = models.Voluntary.objects.all()
        type_expense = models.Type_expense.objects.all()
        return render(request,"beneficiaryapp/expense/create_expense_beneficiary.html",{
            'voluntaries':voluntaries,
            'type_expense':type_expense,
            'beneficiary':beneficiary,
        })


def list_expense_beneficiary(request):
    expenses = models.ExpenseBeneficiary.objects.all()
    return render(request,"beneficiaryapp/expense/list_expense_beneficiary.html",{
        'expenses':expenses
    })
    
    
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