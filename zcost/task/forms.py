from django import forms


class CostForm(forms.Form):
    cost = forms.DecimalField(required=True, label='Значение себестоимости для передачи', max_digits=12,
                              decimal_places=3)