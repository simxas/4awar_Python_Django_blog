from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Tank
from .forms import TankForm, UpdateTankForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
import shutil
from django.utils import timezone

# TANK VIEW
def tank_360(request, slug):
    instance = get_object_or_404(Tank, slug=slug)

    context = {
        "instance": instance,
    }
    return render(request, "tank.html", context)

# ADD TANK
def tank_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = TankForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "tank_form.html", context)


# UPDATE TANK
def tank_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Tank, slug=slug)
    form = UpdateTankForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save(update_fields=[
            "title", "slug", "description", "iframe",
            "updated", "timestamp",
        ])

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "360°",
        "instance": instance,
        "form": form,
    }
    return render(request, "tank_form.html", context)

# DELETE TANK
def tank_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Tank, slug=slug)

    instance.delete()
    return redirect("posts:list")
