from django import forms
from django.utils.translation import gettext_lazy as _

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):

    def __init__(self,max_stock, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if max_stock:
            self.max_stock = max_stock
            self.fields['quantity'] = forms.TypedChoiceField(
                                         #choices=PRODUCT_QUANTITY_CHOICES,
                                        choices=[(i, str(i)) for i in range(1, max_stock+1)],
                                        coerce=int,
                                        label=_("Quantity"))


    # quantity = forms.TypedChoiceField(
    #                                     #choices=PRODUCT_QUANTITY_CHOICES,
    #                                     choices=[(i, str(i)) for i in range(1, 4)],
    #                                     coerce=int,
    #                                     label=_("Quantity"))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


