from django import forms

class CreateNewPollForm(forms.Form):
    question_text = forms.CharField(required=True)
    date_published = forms.DateField(help_text="When should the poll start?")

