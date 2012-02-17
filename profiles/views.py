# Create your views here.

from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse

from profiles.forms import ContactFormSet

def home(request):
    formset = ContactFormSet(request.POST or None)
    if formset.is_valid():
        formset.save()
        return redirect(reverse("home"))
    return render_to_response("profiles/index.html", RequestContext(request, {
        'formset': formset,
    }))
