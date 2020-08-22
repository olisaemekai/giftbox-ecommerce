from django import forms

class SearchProductForm(forms.Form):
    search = forms.CharField(help_text='Search for a product')