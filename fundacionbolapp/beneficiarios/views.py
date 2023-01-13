from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Persona
# Create your views here.

def index(request):
    lista_personas = Persona.objects.all()
    return render(request,"beneficiarios/index.html",{
        "lista_personas": lista_personas
    })


def detallesBeneficiario(request,persona_id):
    persona = get_object_or_404(Persona,pk=persona_id)
    return render(request,"beneficiarios/detalles.html",{
        "persona": persona
    })