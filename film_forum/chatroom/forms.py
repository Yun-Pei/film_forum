from django import forms
from member.models import *

class RoomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ['uid', 'be_uid']