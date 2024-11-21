from django import forms
from .models import Question, Choice

class CreateNewPollForm(forms.Form):
    question_text = forms.CharField(label="Question:", required=True)
    pub_date = forms.DateField(help_text="When should the poll start?")
    response_1 = forms.CharField(label="Response 1*:", required=True)
    response_2 = forms.CharField(label="Repsonse 2*:")
    response_3 = forms.CharField(required=False)
    response_4 = forms.CharField(required=False)
    response_5 = forms.CharField(required=False)
    response_6 = forms.CharField(required=False)


# FamilyMemberForm from tutorial
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()

# FamilyMemberFormSet from tutorial
ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, fields=['choice_text'], extra=2, can_delete=True)