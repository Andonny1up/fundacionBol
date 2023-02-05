from django.shortcuts import render,HttpResponse
from . import views, forms, models


# Create your views here.
def form_create_beneficiary(request):
    type_cancer = models.Cancer.objects.all()
    return render(request,"beneficiaryapp/create_beneficiary.html",{
        'type_cancer':type_cancer
    })


def form_beneficiary(request):
    return render(request,"beneficiaryapp/form_beneficiary.html",{
        'form_persona': forms.PersonForm,
        'form_bene': forms.BeneficiaryForm,
    })


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
        return HttpResponse("Funciona")

# def contact(request):
#     if request.method=="POST":
#         subject=request.POST["asunto"]
#         message=request.POST["msj"+" "+request.POST["email"]]
#         email_from=settings.EMAIL_HOST_USER
#         recipient_list=["Myemail@gamil.com"]
        
#         send_mail(subject,message,email_from,recipient_list)
#         return render(request,"orderManagement/gracias.html")
#     return render(request,"orderManagement/contact.html",)