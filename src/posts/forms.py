from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        list_a = [category.title, category.title]
        categories_list.append(list_a)
    tuple(categories_list)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=categories_list)
    class Meta:
        model = Post
        # fields = '__all__'
        fields = (
            "title",
            "categories",
            "content",
            "image",
            "video_url",
            "draft",
            "publish",
        )
