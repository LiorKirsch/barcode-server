from django import forms

class PhotoForm(forms.Form):

    image       = forms.ImageField()
    machineID   = forms.CharField(max_length=100)
    
    
    
class BarcodeForm(forms.Form):

    barcode     = forms.CharField(max_length=100)
    machineID   = forms.CharField(max_length=100)
    