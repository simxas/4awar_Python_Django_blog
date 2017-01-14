from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from embed_video.fields import EmbedVideoField

def upload_location(instance, filename):
    if instance.directory == "":
        return "{0}/{1}".format(instance.slug, filename)
    else:
        return "{0}/{1}".format(instance.directory, filename)

class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("games:category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Categories"

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0, null=True, blank=True,)
    width_field = models.IntegerField(default=0, null=True, blank=True,)
    directory = models.CharField(max_length=120, null=True)
    description = models.TextField()
    instructions = models.TextField()
    iframe = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    categories = models.ManyToManyField(Category, blank=True, null=True, through='CategoryToGame')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("games:detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Games"
        ordering = ["-timestamp", "-updated"]

class CategoryToGame(models.Model):
    game = models.ForeignKey(Game)
    category = models.ForeignKey(Category)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Game.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{0}-{1}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_game_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.directory = instance.slug

pre_save.connect(pre_save_game_receiver, sender=Game)
