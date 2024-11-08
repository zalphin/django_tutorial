from django import forms

class CreateNewPollForm(forms.Form):
    question_text = forms.CharField(label="Question:", required=True)
    pub_date = forms.DateField(help_text="When should the poll start?")
    response_1 = forms.CharField()
    response_2 = forms.CharField()
    response_3 = forms.CharField()
