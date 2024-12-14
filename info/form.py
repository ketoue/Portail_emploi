from django import forms
from .models import Info

#form to update resume
class UpdateInfoForm(forms.ModelForm):
    class Meta:
      model=Info
      exclude=('user',)
      
      

#form to update for resume besore apply
class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        exclude=('user',)
        
        
    
