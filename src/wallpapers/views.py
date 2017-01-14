from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Wallpaper, Category, CategoryToWallpaper
from .forms import WallpaperForm, UpdateWallpaperForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
import shutil
from django.utils import timezone

def search(request, queryset_list, query):
    categories_list = Category.objects.all()
    queryset_list = queryset_list.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(slug__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 6)
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
        "title": query,
        "categories_list": categories_list,
        "page_request_var": page_request_var,
        "wallpapers": queryset,
    }
    return {"template": "wallpapers_search.html", "context": context}

# Wallpapers VIEW
def wallpapers(request):
    categories_list = Category.objects.all()

    # searc part
    queryset_list = Wallpaper.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    paginator = Paginator(queryset_list, 6)
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
        "wallpapers": queryset,
        "categories_list": categories_list,
        "title": "Wallpapers",
        "page_request_var": page_request_var,
    }

    return render(request, "wallpapers.html", context)

# Wallpaper VIEW
def wallpaper_detail(request, slug):
    instance = get_object_or_404(Wallpaper, slug=slug)
    categories_list = Category.objects.all()

    # searc part
    queryset_list = Wallpaper.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    context = {
        "categories_list": categories_list,
        "instance": instance,
    }
    return render(request, "wallpaper.html", context)

# Wallpaper by CATEGORY
def wallpaper_category(request, slug):
    categories_list = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)

    # searc part
    queryset_list = Wallpaper.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    wallpapers = Wallpaper.objects.filter(categories=category)

    paginator = Paginator(wallpapers, 3) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        wallpapers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        wallpapers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        wallpapers = paginator.page(paginator.num_pages)

    context = {
        "title": category.title,
        "categories_list": categories_list,
        "page_request_var": page_request_var,
        "wallpapers": wallpapers,
    }
    return render(request, "wallpaper_category.html", context)

# CREATE Wallpaper
def wallpaper_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = WallpaperForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        for category in form.cleaned_data.get('categories'):
            # categoryToPost = CategoryToPost(post=instance, category=category)
            # fixing error "Cannot assign "'Tanks'": "CategoryToPost.category" must be a "Category" instance."
            catg = get_object_or_404(Category, title=category)
            categoryToWallpaper = CategoryToWallpaper(wallpaper=instance, category=catg)

            categoryToWallpaper.save()

        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "wallpaper_form.html", context)


# UPDATE Wallpaper
def wallpaper_update(request, slug):
    remove_image = False
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Wallpaper, slug=slug)
    form = UpdateWallpaperForm(request.POST or None, request.FILES or None, instance=instance)
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
            "title", "slug", "image", "height_field", "width_field", "description", "updated", "timestamp",
        ])

        for category in form.cleaned_data.get('categories'):
            # fixing error "Cannot assign "'Tanks'": "CategoryToPost.category" must be a "Category" instance."
            catg = get_object_or_404(Category, title=category)
            categoryToWallpaper = CategoryToWallpaper(wallpaper=instance, category=catg)

            categoryToWallpaper.save()

        for cat in form.cleaned_data.get('rm_categories'):
            category_rm = get_object_or_404(Category, title=cat)
            categoryToWallpaper_rm = CategoryToWallpaper.objects.get(wallpaper=instance, category=category_rm)
            categoryToWallpaper_rm.delete()

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Detail",
        "instance": instance,
        "form": form,
    }
    return render(request, "wallpaper_form.html", context)

# DELETE Wallpaper
def wallpaper_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Wallpaper, slug=slug)
    # removing associated image
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.directory)
    shutil.rmtree(dest, ignore_errors=True)

    instance.delete()
    return redirect("wallpapers:wallpapers")
