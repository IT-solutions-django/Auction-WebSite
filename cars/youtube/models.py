from django.db import models
from googleapiclient.discovery import build
from django.core.exceptions import ObjectDoesNotExist


# AIzaSyDGoDx4ioYPPHyv8bo3wzZLZf1HwenuUA8


class GoogleSettings(models.Model):
    api_key = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Google Settings"

    def __str__(self):
        return f"Google API Settings - {self.api_key}"  

    @classmethod
    def get_instance(cls):
        try:
            return cls.objects.get()
        except ObjectDoesNotExist:
            instance = cls(api_key='YOUR_DEFAULT_API_KEY')  
            instance.save()
            return instance

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    videos = models.ManyToManyField('Video', related_name='playlists',null=True,blank=True)
    google_settings = models.ForeignKey(GoogleSettings, on_delete=models.CASCADE, related_name='playlists')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_videos(video_ids=self.videos.all())  

    def save_videos(self, video_ids):
        self.videos.clear()
        for video in video_ids:
            video_data = self.get_video_data(video.video_url, self.google_settings.api_key)
            if video_data:  
                video_instance, created = Video.objects.get_or_create(youtube_id=video_data['youtube_id'], defaults=video_data)
                self.videos.add(video_instance)

    def get_video_data(self, video_url, api_key):
        video_id = video_url.split('=')[1]
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(part='snippet,statistics', id=video_id)
        
        try:
            response = request.execute()
            video_data = response['items'][0]
            return {
                'youtube_id': video_data['id'],
                'title': video_data['snippet']['title'],
                'description': video_data['snippet']['description'],
                'thumbnail_url': video_data['snippet']['thumbnails']['default']['url'],
                'published_at': video_data['snippet']['publishedAt'],
            }
        except IndexError:
            return None  

class Video(models.Model):
    youtube_id = models.CharField(max_length=255, editable=False)  
    video_url = models.URLField()
    title = models.CharField(max_length=255, editable=False)
    description = models.TextField(editable=False)
    thumbnail_url = models.URLField(editable=False)
    published_at = models.DateTimeField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.youtube_id:  # Обновляем только если youtube_id не задан
            video_data = self.get_video_data(self.video_url, GoogleSettings.get_instance().api_key)
            print(video_data)
            if video_data:
                self.youtube_id = video_data['id']
                self.title = video_data['snippet']['title']
                self.description = video_data['snippet']['description']
                self.thumbnail_url = video_data['snippet']['thumbnails']['default']['url']
                self.published_at = video_data['snippet']['publishedAt']
        super().save(*args, **kwargs)

    @staticmethod
    def get_video_data(video_url, api_key):
        video_id = video_url.split('=')[1]
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.videos().list(part='snippet,statistics', id=video_id)
        response = request.execute()
        return response['items'][0] if response['items'] else None