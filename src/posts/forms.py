from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    # what is this?
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "video_url",
            "draft",
            "publish",
        ]