from celery.schedules import crontab
from settings.settings import app

app.conf.beat_schedule = {
    'update-vk-playlists-every-24-hours': {
        'task': 'vk.tasks.update_playlist_and_videos',
        'schedule': crontab(hour=0, minute=0)
        # Запускать каждый день в полночь
    },
}
