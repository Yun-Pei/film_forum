from django import forms
from forum.models import ForumsMessage

class MessageForm(forms.ModelForm):
        
        class Meta:
            model = ForumsMessage
            fields = ('message_content',)