from django.forms import ModelForm
from .models import Space


class SpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = '__all__'
        exclude = ['host', 'participants']