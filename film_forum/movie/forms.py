from django import forms
from forum.models import Forums

class ForumsForm(forms.ModelForm):
        
        class Meta:
            model = Forums
            fields = ('title', 'content')