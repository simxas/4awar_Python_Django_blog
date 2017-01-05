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
        if len(inst_categories) != 0:
            print("=======================================")
            for category in all_categories:
                for category2 in inst_categories:
                    if category2.title != category.title:
                        print(category2.title)
                        list_a = [category.title, category.title]
                        categories_list.append(list_a)
                    else:
                        pass
        else:
            for category in all_categories:
                print("TUSCIA, postas neturi kategoriju")
                list_a = [category.title, category.title]
                categories_list.append(list_a)
        tuple(categories_list)
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields["title"] = forms.CharField(label="Title", max_length=120)
        self.fields["categories"] = forms.MultipleChoiceField(label="Add Categories", widget=forms.CheckboxSelectMultiple, required=False, choices=categories_list)
        self.fields["content"] = forms.CharField(label="Content", required=False, widget=forms.Textarea)
        self.fields["image"] = forms.ImageField(label="Image")
        self.fields["video_url"] = forms.URLField(required=False)
        self.fields["draft"] = forms.BooleanField()
        self.fields["publish"] = forms.DateField(widget=forms.SelectDateWidget())
