from django import forms
# from forum.models import Forums
from member.models import *

class ForumsForm(forms.ModelForm):
        
        class Meta:
            model = Article
            fields = ('title', 'conent')

# class MovieCommentCont(forms.ModelForm):
        
#         class Meta:
#             model = MovieComment
#             fields = ('conent', )
#             # fields = '__all__'
#             # fields = ('message_content', 'm_id', 'f_id',)
#             # exclude = ['time']
#             widgets = {
#                 'conent': forms.TextInput(attrs={
#                     'id': 'post-text', 
#                     'required': True, 
#                     'placeholder': 'Say something...'
#                 }),
#             }