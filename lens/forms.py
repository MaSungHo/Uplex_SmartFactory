from django import forms
from .models import Image

class ImageForm(forms.Form):
    class Meta:
        model = Image
