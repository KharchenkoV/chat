from django.forms import ModelForm, DecimalField
from django.forms.widgets import Select
from .models import Room, Message

class RoomForm(ModelForm):
    class Meta:
        model = Room