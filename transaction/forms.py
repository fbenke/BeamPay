from django import forms


class CommentInlineFormset(forms.models.BaseInlineFormSet):

    def save_new(self, form, commit=True):
        obj = super(CommentInlineFormset, self).save_new(form, commit=False)
        obj.author = self.request.user
        obj.save()
        return obj


class TransactionModelForm(forms.ModelForm):

    def clean(self):
        if self.cleaned_data['cost_of_delivery_ghs'] and self.cleaned_data['cost_of_delivery_usd']:
            raise forms.ValidationError('Please specify the cost of delivery either in GHS or USD.')
        return self.cleaned_data
