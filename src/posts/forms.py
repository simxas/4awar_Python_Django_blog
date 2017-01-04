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

class UpdateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=120)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                         choices=[])
    content = forms.CharField(label="Content", required=False, widget=forms.Textarea)
    image = forms.ImageField(label="Image")
    video_url = forms.URLField(required=False)
    draft = forms.BooleanField()
    publish = forms.DateField(widget=forms.SelectDateWidget())

    # categories = forms.ModelChoiceField(queryset=None)

    # def __init__(self):
        # super(UpdateForm, self).__init__()
        # self.fields['categories'].queryset = Item.objects.filter(id=item_id)
        # self.fields['categories'].choices = categories
        # print("===============================")
        # print(inst)
