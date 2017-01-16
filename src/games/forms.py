from django import forms
from .models import Game, Category

class GameForm(forms.ModelForm):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        list_a = [category.title, category.title]
        categories_list.append(list_a)
    tuple(categories_list)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=categories_list, required=False)
    class Meta:
        model = Game
        fields = (
            "title",
            "description",
            "instructions",
            "categories",
            "iframe",
            "image",
        )

class UpdateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ["updated", "directory"]


    def __init__ (self, *args, **kwargs):
        all_categories = Category.objects.all()
        instance = kwargs["instance"]

        inst_categories = instance.categories.all()
        categories_list = []
        rm_categories_list = []

        if len(inst_categories) != 0:
            for catg in inst_categories:
                list_b = [catg.title, catg.title]
                rm_categories_list.append(list_b)

            for category in all_categories:
                if category not in inst_categories:
                    list_a = [category.title, category.title]
                    categories_list.append(list_a)
        else:
            for category in all_categories:
                list_a = [category.title, category.title]
                categories_list.append(list_a)
        tuple(categories_list)
        tuple(rm_categories_list)

        super(UpdateGameForm, self).__init__(*args, **kwargs)
        self.fields["title"] = forms.CharField(label="Title", max_length=120)
        self.fields["categories"] = forms.MultipleChoiceField(label="Add Categories",
            widget=forms.CheckboxSelectMultiple, required=False, choices=categories_list)
        self.fields["rm_categories"] = forms.MultipleChoiceField(label="Remove categories",
            widget=forms.CheckboxSelectMultiple, required=False, choices=rm_categories_list)
        self.fields["description"] = forms.CharField(label="Description", required=False, widget=forms.Textarea)
        self.fields["instructions"] = forms.CharField(label="Instructions", required=False, widget=forms.Textarea)
        self.fields["image"] = forms.ImageField(label="Image", required=False)
        self.fields["image_rm"] = forms.BooleanField(label="Remove current Image", required=False)
        if instance.image:
            del self.fields["image"]
        else:
            del self.fields["image_rm"]
