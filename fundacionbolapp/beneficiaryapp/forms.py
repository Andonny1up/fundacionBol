from django import forms
from . import models

#Creating a form
class PersonForm(forms.ModelForm):
    
    #create meta class
    class Meta:
        #specify model to be used
        model = models.Person
        
        #specify fields to be used
        fields="__all__"


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = models.Beneficiary
        
        #specify fields to be used
        fields="__all__"
        
    
#Example:::       
"""     
# creating a form
class GeeksForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = GeeksModel

		# specify fields to be used
		fields = [
			"title",
			"description",
		]
"""