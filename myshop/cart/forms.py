from django import forms
from django.utils.translation import gettext_lazy as _

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):

    def __init__(self, max_stock=None, *args, **kwargs):

        super(CartAddProductForm, self).__init__(*args, **kwargs)


        if max_stock:
            # print(max_stock)
            self.max_stock = max_stock
            # print(self.max_stock)
            #print(*args)
            self.fields['quantity'] = forms.TypedChoiceField(
                                         #choices=PRODUCT_QUANTITY_CHOICES,
                                        choices=[(i, str(i)) for i in range(1, self.max_stock+1)],
                                        coerce=int,
                                        label=_("Quantity"))
        else:
            self.fields['quantity'] = forms.TypedChoiceField(
                # choices=PRODUCT_QUANTITY_CHOICES,
                choices=[(i, str(i)) for i in range(1, 21)],
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


