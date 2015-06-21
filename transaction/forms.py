from django.contrib.contenttypes import forms


class CommentInlineFormset(forms.BaseGenericInlineFormSet):

    def save_new(self, form, commit=True):
        obj = super(CommentInlineFormset, self).save_new(form, commit=False)
        obj.author = self.request.user
        obj.save()
        return obj
