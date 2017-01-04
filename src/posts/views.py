from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, CategoryToPost
from .forms import PostForm, UpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.conf import settings
import shutil
from django.utils import timezone

# LIST ALL POSTS
def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    # using this for search
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list, 10)
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
        "object_list": queryset,
        "title": "Prisijunges",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "posts_list.html", context)

# CHECK POST DETAILS
def post_detail(request, slug):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "title": instance.title,
        "instance": instance,
        "today": today,
        "slug": slug,
    }
    return render(request, "post_detail.html", context)

def post_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category)

    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
            ).distinct()

    context = {
        "title": category.title,
        "posts": posts,
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
            # categoryToPost = CategoryToPost(post=instance, category=category)
            # fixing error "Cannot assign "'Tanks'": "CategoryToPost.category" must be a "Category" instance."
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    # form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    '''
    form = UpdateForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        # print("===================")
        # print(form.cleaned_data.get('categories'))
        # instance.save()

        for category in form.cleaned_data.get('categories'):

            # for categ in instance.categories.all():
            #     if categ.title == category:
            #         categ = category
            #         print(categ)
            #
            # print("======================")
            # print(category)
            # fixing error "Cannot assign "'Tanks'": "CategoryToPost.category" must be a "Category" instance."
            catg = get_object_or_404(Category, title=category)
            categoryToPost = CategoryToPost(post=instance, category=catg)

            categoryToPost.save()
        instance.save()
    '''
    # TEST CODE================
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UpdateForm(request.POST, categories=(("a", "b"), ("a", "b")))
        # check whether it's valid:
        if form.is_valid():
            instance = form.save(commit=False)
            for category in form.cleaned_data.get('categories'):
                # fixing error "Cannot assign "'Tanks'": "CategoryToPost.category" must be a "Category" instance."
                catg = get_object_or_404(Category, title=category)
                categoryToPost = CategoryToPost(post=instance, category=catg)
                categoryToPost.save()
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())

    # if a GET (or any other method) we'll create a blank form
    else:
        data = {'title': 'hello'}
        form = UpdateForm(data)
    # TEST CODE================



        # return HttpResponseRedirect(instance.get_absolute_url())

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
    # removing associated image
    dest = "{0}/{1}".format(settings.MEDIA_ROOT, instance.slug)
    shutil.rmtree(dest, ignore_errors=True)

    instance.delete()
    return redirect("posts:list")
