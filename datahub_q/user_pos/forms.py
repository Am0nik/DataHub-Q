from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nickname', 'text']
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': 'Ваш ник'}),
            'text': forms.Textarea(attrs={'placeholder': 'Ваш комментарий', 'rows': 3}),
        }