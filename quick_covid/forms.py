from django import forms
from quick_covid.models import Location


class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ('name',)


class LocationSelectForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label='')
 
    # class Meta:
    #     model = Location
