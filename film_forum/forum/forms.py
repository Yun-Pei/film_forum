# from django import forms
# from forum.models import ForumsMessage

# class MessageForm(forms.ModelForm):
        
#         class Meta:
#             model = ForumsMessage
#             fields = ('message_content', )
#             # fields = '__all__'
#             # fields = ('message_content', 'm_id', 'f_id',)
#             # exclude = ['time']
#             widgets = {
#                 'message_content': forms.TextInput(attrs={
#                     'id': 'post-text', 
#                     'required': True, 
#                     'placeholder': 'Say something...'
#                 }),
#             }