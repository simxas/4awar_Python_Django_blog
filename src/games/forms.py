from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = (
            "title",
            "description",
            "instructions",
            "iframe",
            "image",
        )

class UpdateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ["updated", "directory"]


    def __init__ (self, *args, **kwargs):
        # foo = kwargs.pop("instance")
        instance = kwargs["instance"]

        super(UpdateGameForm, self).__init__(*args, **kwargs)
        self.fields["title"] = forms.CharField(label="Title", max_length=120)
        self.fields["description"] = forms.CharField(label="Description", required=False, widget=forms.Textarea)
        self.fields["instructions"] = forms.CharField(label="Instructions", required=False, widget=forms.Textarea)
        self.fields["image"] = forms.ImageField(label="Image", required=False)
        self.fields["image_rm"] = forms.BooleanField(label="Remove current Image", required=False)
        if instance.image:
            del self.fields["image"]
        else:
            del self.fields["image_rm"]
