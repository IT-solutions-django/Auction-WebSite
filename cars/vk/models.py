from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class VkSettings(models.Model):
    url = models.URLField()
    api_key = models.TextField(null=False, blank=False)

    def __str__(self):
        return ('Настройки для канала ' + self.url)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        try:
            return cls.objects.get()
        except ObjectDoesNotExist:
            instance = cls(api_key='YOUR_DEFAULT_API_KEY')
            instance.save()
            return instance


class PlayList(models.Model):
    titile = models.CharField(max_length=255, null=False, blank=False)
    videos_count = models.PositiveIntegerField(editable=False)
    videos = models.ManyToManyField('Video', null=True, blank=True)
    vk_settings = models.ForeignKey(
        VkSettings,
        on_delete=models.CASCADE,
        related_name='playlists'
    )

    def __str__(self):
        return self.titile


class Video(models.Model):
    url = models.TextField(editable=False)
    preview = models.TextField(editable=False)

    duration = models.PositiveIntegerField(editable=False)
    description = models.TextField(editable=False)

    title = models.CharField(max_length=255, editable=False)
    id = models.PositiveBigIntegerField(editable=False, primary_key=True)

    def __str__(self):
        return (f'{self.title}  {self.id}')
