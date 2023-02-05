from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Persona
from .forms import PersonaForm
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
    
def create_persona(request):
    	# dictionary for initial data with
	# field names as keys
	context ={}

	# add the dictionary during initialization
	form = PersonaForm(request.POST or None)
	if form.is_valid():
		form.save()
		
	context['form']= form
	return render(request, "beneficiarios/create_persona.html", context)