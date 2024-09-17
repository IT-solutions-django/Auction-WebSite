import requests
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VkSettings, PlayList, Video


@receiver(post_save, sender=VkSettings)
def create_playlists_and_videos(sender, instance, created, **kwargs):
        with transaction.atomic():
            PlayList.objects.all().delete()
            Video.objects.all().delete()

        community_id = instance.url.split("/")[-1]
        if "@" in community_id:
            community_id = community_id.split("@")[1]

        headers = {"Authorization": "Bearer " + instance.api_key}
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
            album_id = album["id"]
            videos_response = requests.get(
                f"https://api.vk.com/method/video.get?owner_id=-{id_}&album_id={album_id}&v=5.131",
                headers=headers,
                # proxies=proxies,
            )
            video_count = videos_response.json()["response"]["count"]
            playlist = PlayList.objects.create(
                titile=album["title"],
                vk_settings=instance,
                videos_count=video_count
            )
            videos = videos_response.json()["response"]["items"]

            for video in videos:
                vid = Video.objects.create(
                    url=video["player"],
                    preview=video["image"][0]["url"],
                    duration=video["duration"],
                    description=video["description"],
                    title=video["title"],
                    id=video["id"],
                )
                playlist.videos.add(vid)
