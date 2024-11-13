from django import forms

class CreateNewPollForm(forms.Form):
    question_text = forms.CharField(label="Question:", required=True)
    pub_date = forms.DateField(help_text="When should the poll start?")
    response_1 = forms.CharField(label="Response 1*:", required=True)
    response_2 = forms.CharField(label="Repsonse 2*:")
    response_3 = forms.CharField(required=False)
    response_4 = forms.CharField(required=False)
    response_5 = forms.CharField(required=False)
    response_6 = forms.CharField(required=False)
