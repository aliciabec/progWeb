from django import forms

class MyForm(forms.Form):
    my_field = forms.ChoiceField(
        choices=[('r1', 'genome'), ('r2', 'gene_prot')],
        widget=forms.RadioSelect,
    )
