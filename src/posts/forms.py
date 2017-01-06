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
    publish = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Post
        fields = (
            "title",
            "categories",
            "content",
            "image",
            "video_url",
            "draft",
            "publish",
        )

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["updated"]


    def __init__ (self, *args, **kwargs):
        # foo = kwargs.pop("instance")
        all_categories = Category.objects.all()
        instance = kwargs["instance"]
        inst_categories = instance.categories.all()
        categories_list = []
        # check if post has already some cateogires assigned to it
        if len(inst_categories) != 0:
            for category in all_categories:
                # if category wont exist in assigned categories list then add it to the list to show in form
                if category not in inst_categories:
                    # needs to be done in order to create a tuple later
                    list_a = [category.title, category.title]
                    categories_list.append(list_a)
        else:
            for category in all_categories:
                list_a = [category.title, category.title]
                categories_list.append(list_a)
        tuple(categories_list)
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields["title"] = forms.CharField(label="Title", max_length=120)
        self.fields["categories"] = forms.MultipleChoiceField(label="Add Categories",
            widget=forms.CheckboxSelectMultiple, required=False, choices=categories_list)
        self.fields["content"] = forms.CharField(label="Content", required=False, widget=forms.Textarea)
        self.fields["image"] = forms.ImageField(label="Image")
        self.fields["video_url"] = forms.URLField(required=False)
        self.fields["draft"] = forms.BooleanField()
        self.fields["publish"] = forms.DateField(widget=forms.SelectDateWidget())
