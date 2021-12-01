from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name']



class SignUpForm(UserCreationForm):
    # My Own Custom Fields
    username = forms.Field(widget=forms.TextInput(attrs={'class':'form-control'}), label='Логін')
    first_name = forms.CharField(label='Ім\'я')
    last_name=forms.CharField(label='Прізвище')
    email=forms.EmailField(label='Електрона пошта')
    # The Default Fields Of The UserCreation Form
    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

