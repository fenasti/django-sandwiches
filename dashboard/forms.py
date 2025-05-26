from django import forms

class SalesDataForm(forms.Form):
    cheese_ham = forms.IntegerField(label='Cheese Ham')
    tom_moz = forms.IntegerField(label='Tom Moz')
    chicken_salad = forms.IntegerField(label='Chicken Salad')
    egg_salad = forms.IntegerField(label='Egg Salad')
    hummus_veg = forms.IntegerField(label='Hummus Veg')
    ham_egg = forms.IntegerField(label='Ham Egg')

# class SalesDataForm(forms.Form):
#     sales_data = forms.CharField(
#         label='Enter sales data (6 numbers, comma-separated)',
#         help_text='Example: 10,20,30,40,50,60'
#     )