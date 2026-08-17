from django import forms

from .models import MangoUsersModel


class MangoUsersModelForm(forms.ModelForm):
    class Meta:
        model = MangoUsersModel
        fields = ['name', 'title', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age', 'min': 0}),
        }
