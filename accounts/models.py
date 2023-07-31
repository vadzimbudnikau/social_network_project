from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """User profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_profiles', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_profiles', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username



