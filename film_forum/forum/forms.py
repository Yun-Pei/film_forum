from django import forms
from member.models import *

class MessageForm(forms.ModelForm):
        
        class Meta:
            model = ArticleComment
            fields = ('conent', )
            # fields = '__all__'
            # fields = ('message_content', 'm_id', 'f_id',)
            # exclude = ['time']
            widgets = {
                'conent': forms.TextInput(attrs={
                    'id': 'post-text', 
                    'required': True, 
                    'placeholder': 'Say something...'
                }),
            }