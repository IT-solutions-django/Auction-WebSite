from celery import shared_task
from django.db import transaction
from .models import VkSettings, PlayList, Video
import requests


@shared_task
def update_playlists_and_videos():
    with transaction.atomic():

        PlayList.objects.all().delete()
        Video.objects.all().delete()

    settings = VkSettings.get_instance()
    community_id = settings.url.split("/")[-1]
    if "@" in community_id:
        community_id = community_id.split("@")[1]

    headers = {"Authorization": "Bearer " + settings.api_key}
    proxy = "138.219.123.120:9546"
    # proxies = {"http": proxy, "https": proxy}

    response = requests.get(
        f"https://api.vk.com/method/groups.getById?group_ids={community_id}&v=5.131",
        headers=headers,
        # proxies=proxies,
    )
    data = response.json()
    id_ = data["response"][0]["id"]

    albums_response = requests.get(
        f"https://api.vk.com/method/video.getAlbums?owner_id=-{id_}&v=5.131",
        headers=headers,
        # proxies=proxies,
    )
    albums = albums_response.json()["response"]["items"]

    for album in albums:
        videos_response = requests.get(
            f'https://api.vk.com/method/video.get?owner_id=-{id_}&album_id={album["id"]}&v=5.131',
            headers=headers,
            # proxies=proxies,
        )
        video_count = videos_response.json()["response"]["count"]
        playlist, created = PlayList.objects.get_or_create(
            titile=album["title"], vk_settings=settings, videos_count=video_count
        )
        videos = videos_response.json()["response"]["items"]

        for video in videos:
            video_obj, _ = Video.objects.update_or_create(
                id=video["id"],
                defaults={
                    "url": video["player"],
                    "preview": video["image"][0]["url"],
                    "duration": video["duration"],
                    "description": video["description"],
                    "title": video["title"],
                },
            )
            playlist.videos.add(video_obj)
