from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = [
        #     "title",
        #     "categories",
        #     "content",
        #     "image",
        #     "video_url",
        #     "draft",
        #     "publish",
        # ]
