from django import forms

from map_locator.map.models import Search


class SearchForm(forms.ModelForm):
    address = forms.CharField(label='')

    class Meta:
        model = Search
        fields = ['address', ]
