from django import forms
from .models import Plant
from .models import Comment


class PlantForm(forms.ModelForm):

    class Meta:
        model = Plant
        fields = ['name', 'description', 'sunlight', 'size', 'price', 'plant_picture', 'timestamp']
        widgets = {
            'sunlight': forms.Select(choices=Plant.SUNLIGHT),
            'myuser': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['stars', 'text']
        widgets = {
            'myuser': forms.HiddenInput(),
            'plant': forms.HiddenInput(),
        }


class SearchForm(forms.ModelForm):
    stars = forms.IntegerField(label='Stars',required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = Plant
        fields = ['name', 'description', 'stars']