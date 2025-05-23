from django import forms

class SalesDataForm(forms.Form):
    sales_data = forms.CharField(
        label='Enter sales data (6 numbers, comma-separated)',
        help_text='Example: 10,20,30,40,50,60'
    )