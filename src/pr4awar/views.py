from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# contact view
def contact(request):
    context = {
        "title": "Contact",
    }
    return render(request, "contact.html", context)
