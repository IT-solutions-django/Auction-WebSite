from django import forms
from .models import Video
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_id']

    def clean_video_id(self):
        video_id = self.cleaned_data.get('video_id')
        return video_id