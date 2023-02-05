from django import forms
from .models import Persona


# creating a form
class PersonaForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Persona

		# specify fields to be used
		fields = "__all__"