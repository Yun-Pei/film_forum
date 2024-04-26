from django import forms
from forum.models import ForumsMessage

class MessageForm(forms.ModelForm):
        
        class Meta:
            model = ForumsMessage
            fields = '__all__'
            # fields = ('message_content', 'm_id', 'f_id',)