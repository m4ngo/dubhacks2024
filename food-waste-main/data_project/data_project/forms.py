from django import forms
from .models import SignUp, currentQuests

class userSignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['name', 'phone', 'street', 'city', 'state', 'zip', 'password']

class create_quest_form(forms.ModelForm):
    class Meta:
        model = currentQuests
        fields = ['item']


