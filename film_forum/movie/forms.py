from django import forms
# from forum.models import Forums
from member.models import *

class ForumsForm(forms.ModelForm):
        
        class Meta:
            model = Article
            fields = ('title', 'conent')