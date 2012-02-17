from django import forms

from django.forms.models import BaseModelFormSet, modelformset_factory

from profiles.models import Email, Contact

EmailFormSet = modelformset_factory(Email, can_delete=True)


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.formset = kwargs.pop('formset', None)

    class Meta:
        model = Contact


class BaseContactFormSet(BaseModelFormSet):
    """
    Handles nested formsets
    """

    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            data = self.data or None
            prefix = 'email_formset_%s' % (i)
            formset = EmailFormSet(data, prefix=prefix)
            extra_kwargs = {
                'formset': formset
            }
            self.forms.append(self._construct_form(i, **extra_kwargs))

    def is_valid(self):
        for form in self.forms:
            if not form.formset.is_valid():
                return False
        return super(BaseContactFormSet, self).is_valid()

    def save_formsets(self, instance, form):
        emails = form.formset.save()
        instance.emails.add(emails)
        return instance

    def save_new(self, form, commit=True):
        instance = super(BaseContactFormSet, self).save_new(form, commit)
        self.save_formsets(instance, form)
        return instance

    def save_existing(self, form, instance, commit=True):
        instance = super(BaseContactFormSet, self).save_existing(form, commit)
        self.save_formsets(instance, form)
        return instance

ContactFormSet = modelformset_factory(Contact, form=ContactForm, can_delete=True, formset=BaseContactFormSet)
