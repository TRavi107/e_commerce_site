from django import forms

PAYMENT_OPTIONS = (
    ('S','Stripe'),
    ('P','Paypall')
)

class Checkoutform(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St'
    }))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'Apartment or Suite'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTIONS)

class CommentForm(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Write your comment here!',
        'class':'pb-cmnt-textarea'
    }))