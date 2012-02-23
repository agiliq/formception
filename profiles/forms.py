from django import forms

from django.forms.models import BaseModelFormSet, modelformset_factory

from profiles.models import Email, Contact

EmailFormSet = modelformset_factory(Email, can_delete=True)


class ContactForm(forms.ModelForm):
    """
    We have overriden init to take the nested email formset
    as a parameter. This makes sure that each contact formset is related
    to each email formset.
    """

    def __init__(self, *args, **kwargs):
        self.formset = kwargs.pop('formset', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
        exclude = ["emails", ] # We don't need emails in the form anymore


class BaseContactFormSet(BaseModelFormSet):
    """
    This base formset is resposible for handling the email formset
    belonging to each contact formset
    """

    def _construct_forms(self):
        """
        Create an email formset and pass it to the
        contact form as a extra kwarg, also restrict
        the queryset to related objects only
        """
        self.forms = []
        for i in xrange(self.total_form_count()):
            data = self.data or None
            prefix = 'email_formset_%s' % (i)
            queryset = self.get_queryset()
            qs = Email.objects.none()
            if queryset:
                if len(queryset) > i:
                    instance = queryset[i]
                    qs = instance.emails.all()
            formset = EmailFormSet(data, prefix=prefix, queryset=qs)
            extra_kwargs = {
                'formset': formset
            }
            self.forms.append(self._construct_form(i, **extra_kwargs))

    def is_valid(self):
        """
        For the formset to be valid, each form in the nested
        formset should also be valid
        """
        for form in self.forms:
            if not form.formset.is_valid():
                return False
        return super(BaseContactFormSet, self).is_valid()

    def save_formsets(self, instance, form):
        """
        Save the formset and attach the results to the instance
        """
        emails = form.formset.save()
        instance.emails.add(*emails)
        return instance

    def save_new(self, form, commit=True):
        """
        Save formsets
        """
        instance = super(BaseContactFormSet, self).save_new(form, commit)
        self.save_formsets(instance, form)
        return instance

    def save_existing(self, form, instance, commit=True):
        """
        Save formsets
        """
        instance = super(BaseContactFormSet, self).save_existing(form, commit)
        self.save_formsets(instance, form)
        return instance

ContactFormSet = modelformset_factory(Contact, form=ContactForm, can_delete=True, formset=BaseContactFormSet)
