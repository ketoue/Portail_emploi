from django import forms
from .models import Staf

from django import forms
from .models import Staf


#form to update a company
class UpdateStafForm(forms.ModelForm):
    class Meta:
        model = Staf
        fields = ['name', 'est_date', 'ville', 'province']  
