from django import forms
from .models import p_img

class img_form(forms.ModelForm):
    class Meta:
        model = p_img
        fields = ['image', 'desc']

