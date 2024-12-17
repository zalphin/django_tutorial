from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "pub_date"]
        widgets = {
            'pub_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }
        # field_classes = {
        #     "pub_date": ""
        # }
    # question_text = forms.CharField(label="Question:", required=True)
    # pub_date = forms.DateField(help_text="When should the poll start?")


# FamilyMemberForm from tutorial
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ()

# FamilyMemberFormSet from tutorial
ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, fields=['choice_text'], extra=1, can_delete=True)