from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, CategoryToPost
from .forms import PostForm, UpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
import shutil
from django.utils import timezone

# CUSTOM FUNCTIONS
def search(request, queryset_list, query):
    today = timezone.now().date()
    categories_list = Category.objects.all()
    queryset_list = queryset_list.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__first_name__icontains=query) |
        Q(author__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "title": query,
        "categories_list": categories_list,
        "page_request_var": page_request_var,
        "posts": queryset,
        "today": today,
    }
    return {"template": "post_search.html", "context": context}

# LIST ALL POSTS
def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    categories_list = Category.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "posts": queryset,
        "categories_list": categories_list,
        "title": "Prisijunges",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "posts_list.html", context)

# CHECK POST DETAILS
def post_detail(request, slug):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    categories_list = Category.objects.all()

    # searc part
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "title": instance.title,
        "instance": instance,
        "categories_list": categories_list,
        "today": today,
        "slug": slug,
    }
    return render(request, "post_detail.html", context)

# POSTS by CATEGORY
def post_category(request, slug):
    print("post category")
    today = timezone.now().date()
    categories_list = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)

    # searc part
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    posts = Post.objects.active(category=category)
    if request.user.is_staff or request.user.is_superuser:
        posts = Post.objects.filter(categories=category)

    paginator = Paginator(posts, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "title": category.title,
        "categories_list": categories_list,
        "page_request_var": page_request_var,
        "posts": posts,
        "today": today,
    }
    return render(request, "post_category.html", context)

# CREATE POST
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        for category in form.cleaned_data.get('categories'):
            catg = get_object_or_404(Category, title=category)
            categoryToPost = CategoryToPost(post=instance, category=catg)

            categoryToPost.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

# UPDATE POST
def post_update(request, slug):
    remove_image = False
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = UpdateForm(request.POST or None, request.FILES or None, instance=instance)
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.directory)
    if form.is_valid():
        if form.cleaned_data.get('image_rm'):
            remove_image = True
            instance.image = ""
            shutil.rmtree(dest, ignore_errors=True)
        if form.cleaned_data.get('image') and remove_image == False:
            instance.image = form.cleaned_data.get('image')
        instance = form.save(commit=False)
        instance.save(update_fields=[
            "title", "slug", "image", "video_url",
            "height_field", "width_field", "content",
            "draft", "publish", "updated", "timestamp",
        ])
        for category in form.cleaned_data.get('categories'):
            catg = get_object_or_404(Category, title=category)
            categoryToPost = CategoryToPost(post=instance, category=catg)

            categoryToPost.save()

        for cat in form.cleaned_data.get('rm_categories'):
            category_rm = get_object_or_404(Category, title=cat)
            categoryToPost_rm = CategoryToPost.objects.get(post=instance, category=category_rm)
            categoryToPost_rm.delete()

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Detail",
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

# DELETE POST
def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.directory)
    shutil.rmtree(dest, ignore_errors=True)

    instance.delete()
    return redirect("posts:list")
