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


def form_beneficiary(request):
    return render(request,"beneficiaryapp/form_beneficiary.html",{
        'form_persona': forms.PersonForm,
        'form_bene': forms.BeneficiaryForm,
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
    return render(request,"beneficiaryapp/details_beneficiary.html",{
        'beneficiary': bene,
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
        c_name =request.POST["c_name"]
        
        person = models.Person.objects.create(dni=dni,name = name,birthday=birthday,gender=gender,phone=phone,address=address)
        cancer = models.Cancer.objects.get(pk=c_name)
        bene= models.Beneficiary.objects.create(id_perso=person,id_cancer=cancer)
        return HttpResponseRedirect(reverse("beneficiary:details_beneficiary",args=(bene.id,)))
    else:
       return render(request,"beneficiaryapp/companion/form_create.html",{
        'beneficiary_id': beneficiary_id
    }) 
# <-- Companion -->
# def contact(request):
#     if request.method=="POST":
#         subject=request.POST["asunto"]
#         message=request.POST["msj"+" "+request.POST["email"]]
#         email_from=settings.EMAIL_HOST_USER
#         recipient_list=["Myemail@gamil.com"]
        
#         send_mail(subject,message,email_from,recipient_list)
#         return render(request,"orderManagement/gracias.html")
#     return render(request,"orderManagement/contact.html",)