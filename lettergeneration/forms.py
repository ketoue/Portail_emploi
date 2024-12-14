from django import forms
from .models import Resume


#form for the generate cover letter
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']


#form for selected a cover letter if a want
class CoverLetterForm(forms.Form):
    add_cover_letter = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
        label="Would you like to add a cover letter?"
    )
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
        label="Cover Letter (optional if 'No' is selected)"
    )