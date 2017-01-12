from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Game
from .forms import GameForm, UpdateGameForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
import shutil
from django.utils import timezone

# GAMES VIEW
def games(request):
    # categories_list = Category.objects.all()

    # searc part
    queryset_list = Game.objects.all()
    # query = request.GET.get("q")
    # if query:
    #     search_dict = search(request, queryset_list, query)
    #     return render(request, search_dict["template"], search_dict["context"])

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "games": queryset,
        # "categories_list": categories_list,
        "title": "Games Page",
        "page_request_var": page_request_var,
    }

    return render(request, "games.html", context)

# GAME VIEW
def game_detail(request, slug):
    instance = get_object_or_404(Game, slug=slug)
    # categories_list = Category.objects.all()

    # searc part
    # queryset_list = Post.objects.active()
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Post.objects.all()
    # query = request.GET.get("q")
    # if query:
    #     search_dict = search(request, queryset_list, query)
    #     return render(request, search_dict["template"], search_dict["context"])

    context = {
        # "categories_list": categories_list,
        "instance": instance,
    }
    return render(request, "game.html", context)

# CREATE GAME
def game_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = GameForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "game_form.html", context)


# UPDATE GAME
def game_update(request, slug):
    remove_image = False
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Game, slug=slug)
    form = UpdateGameForm(request.POST or None, request.FILES or None, instance=instance)
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.directory)
    if form.is_valid():
        if form.cleaned_data.get('image_rm'):
            remove_image = True
            instance.image = ""
            shutil.rmtree(dest, ignore_errors=True)
        # if new image uploaded
        if form.cleaned_data.get('image') and remove_image == False:
            instance.image = form.cleaned_data.get('image')
        instance = form.save(commit=False)
        instance.save(update_fields=[
            "title", "slug", "image", "height_field", "width_field", "description",
            "instructions", "updated", "timestamp",
        ])

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Detail",
        "instance": instance,
        "form": form,
    }
    return render(request, "game_form.html", context)

# DELETE GAME
def game_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Game, slug=slug)
    # removing associated image
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.directory)
    shutil.rmtree(dest, ignore_errors=True)

    instance.delete()
    return redirect("games:games")
