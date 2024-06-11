from django.forms import ModelForm, TextInput, NumberInput
from .models import Expanse

class ExpanseForm(ModelForm):
    class Meta:
        model = Expanse
        fields = ['name', 'amount', 'category']
        widgets = {
            'name': TextInput(attrs={'class': 'mt-1 block w-full sm:flex-auto border border-gray-300 rounded-md py-2 px-3 focus:outline-none'}),
            'amount': NumberInput(attrs={'class': 'mt-1 block w-full sm:flex-auto border border-gray-300 rounded-md py-2 px-3 focus:outline-none'}),
            'category': TextInput(attrs={'class': 'mt-1 block w-full sm:flex-auto border border-gray-300 rounded-md py-2 px-3 focus:outline-none'}),
        }