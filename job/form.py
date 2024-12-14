from django import forms
from .models import Job

#form to create a new job
class CreateJobForm(forms.ModelForm):
    class Meta:
        model=Job
        exclude=('user','staf','timestamp')
        

#form to update a exist job
class UpdateJobForm(forms.ModelForm):
    class Meta:
        model=Job
        exclude=('user','staf','timestamp')
        
        

#form for generate cover letter
class CoverLetterForm(forms.Form):
    add_cover_letter = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Would you like to add a cover letter?"
    )
