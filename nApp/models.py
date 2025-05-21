from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import re
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

    # … your existing fields …
class Video(models.Model):
    title=models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre, related_name="videos", blank=True)
    url=models.URLField(null=True,blank=True)
    @property
    def youtube_id(self):
        """
        Regex pulls out the ID from both:
        - https://www.youtube.com/watch?v=ID
        - https://youtu.be/ID
        """
        pattern = r'(?:v=|youtu\.be/)([^?&]+)'
        match = re.search(pattern, self.url)
        return match.group(1) if match else None

    @property
    def thumbnail_url(self):
        """
        Constructs the standard ‘hqdefault’ thumbnail URL.
        You can also use:
         - /default.jpg       (120×90)
         - /mqdefault.jpg     (320×180)
         - /sddefault.jpg     (640×480)
         - /maxresdefault.jpg (1280×720) – if available
        """
        if not self.youtube_id:
            return ''
        return f'https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg'
    
    @property
    def trailer_mime(self):
        url = self.url or ""
        if url.lower().endswith('.mp4'):
            return 'video/mp4'
        # you could also detect HLS (.m3u8) here
        return 'video/youtube'
    
    def __str__(self):
        return self.title
   