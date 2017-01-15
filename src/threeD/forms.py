from django import forms
from .models import Tank

class TankForm(forms.ModelForm):
    class Meta:
        model = Tank
        fields = (
            "title",
            "description",
            "iframe",
        )

class UpdateTankForm(forms.ModelForm):
    class Meta:
        model = Tank
        exclude = ["updated",]


    def __init__ (self, *args, **kwargs):
        # foo = kwargs.pop("instance")
        instance = kwargs["instance"]

        super(UpdateTankForm, self).__init__(*args, **kwargs)
        self.fields["title"] = forms.CharField(label="Title", max_length=120)
        self.fields["description"] = forms.CharField(label="Description", required=False, widget=forms.Textarea)
