import hashlib
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
from urllib.parse import urlparse

import click
import requests

from src.utils import check_domain_validity, prepare_headers


# Enum declarations
class URLType(Enum):
    VIDEO = "video"
    PLAYLIST = "playlist"


class VideoQuality(Enum):
    FULL_HD = "1080p"
    HD = "720p"
    FOUR_EIGHTY = "480p"
    THREE_SIXTY = "360p"
    TWO_FORTY = "240p"
    ONE_FORTY_FOUR = "144p"


# CONSTANTS
API_BASE_URL = "https://www.aparat.com/api/fa/v1"


class Downloader:
    def __init__(self, url, filename=None) -> None:
        self.file_name = filename
        self.links = []
        self.url = self._cleanup_url(url)
        self.url_type = self._url_type()
        self.videos = self._get_available_videos()
        self.qualities = self._get_available_qualities()

    @staticmethod
    def _cleanup_url(url: str):
        url = url.replace("https://", "").replace("www.", "").rstrip("/")
        return url.split("?", 1)[0]

    def _url_type(self) -> URLType:
        if not check_domain_validity(self.url):
            raise ValueError("Invalid URL")
        if "/v/" in self.url:
            self.video_uid = self.url.rsplit("/", 1)[-1]
            return URLType.VIDEO
        elif "/playlist/" in self.url:
            self.playlist_id = self.url.rsplit("/", 1)[-1]
            return URLType.PLAYLIST
        else:
            raise ValueError("Invalid URL")

    def _get_available_videos(self) -> list:
        if self.url_type == URLType.VIDEO:
            return [self._get_single_video_qualities(self.video_uid)]
        elif self.url_type == URLType.PLAYLIST:
            click.echo("Loading playlist videos")
            all_videos = []
            playlist_data = requests.get(
                f"{API_BASE_URL}/video/playlist/one/playlist_id/{self.playlist_id}",  # noqa
                headers=prepare_headers(),
            ).json()
            video_urls = [
                item
                for item in playlist_data["included"]
                if item["type"] == "Video"  # noqa
            ]

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [
                    executor.submit(
                        self._get_single_video_qualities,
                        video["attributes"]["uid"],
                        self.playlist_id,
                    )
                    for video in video_urls
                ]

            for future in as_completed(futures):
                all_videos.append(future.result())

            return all_videos

    def _get_single_video_qualities(self, video_uid, playlist_id=None):
        query = f"?playlist={playlist_id}&pr=1&mf=1" if playlist_id else ""
        video_data = requests.get(
            f"{API_BASE_URL}/video/video/show/videohash/{video_uid}{query}",
            headers=prepare_headers(),
        ).json()

        video_attrs = video_data["data"]["attributes"]
        return [
            {
                "title": video_attrs["title"],
                "profile": attr.get("profile"),
                "url": attr.get("urls")[0],
            }
            for attr in video_attrs["file_link_all"]
        ]

    def _get_available_qualities(self):
        qualities = {
            video_quality.get("profile")
            for video in self.videos
            for video_quality in video
        }
        return sorted(qualities, key=lambda x: int(x[:-1]))

    def default_quality(self):
        return (
            VideoQuality.HD.value
            if VideoQuality.HD.value in self.qualities
            else self.qualities[-1]
        )

    def find_closest_quality(self, video_list, target_quality):
        exact_quality_videos = [
            video for video in video_list if video["profile"] == target_quality
        ]
        if exact_quality_videos:
            return exact_quality_videos[0]

        video_qualities = [
            int(video["profile"][:-1]) for video in video_list
        ]  # Extract the qualities and convert to integers
        closest_quality = min(
            video_qualities, key=lambda x: abs(x - int(target_quality[:-1]))
        )

        for video in video_list:
            if video["profile"] == str(closest_quality) + "p":
                return video

    def download(self, quality: str):
        for video_qualities in self.videos:
            video = self.find_closest_quality(video_qualities, quality)
            self._download_video(video)

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        # Remove characters that are invalid on common filesystems
        invalid = r'<>:"/\|?*'
        for char in invalid:
            name = name.replace(char, "")
        # Strip trailing dots/spaces and limit length to be safe
        name = name.strip().strip(".")
        if len(name) > 200:
            name = name[:200]
        return name or "video"

    def _download_video(self, video):
        url = video.get("url")
        title = video.get("title")
        click.echo(f"{title}\n{url}")
        file_name = self._sanitize_filename(self.file_name or video.get("title"))
        file_format = self._get_file_format(url)
        output_file = f"{file_name}.{file_format}" if file_format else file_name
        # Check if file already exists
        if os.path.isfile(output_file):
            # Create a hash of the filename
            hash_object = hashlib.md5(output_file.encode())
            hex_dig = hash_object.hexdigest()
            # Append the hash to the filename
            output_file = f"{hex_dig}_{output_file}"
        # Download to a safe temporary file first, then rename. This avoids
        # issues with filesystems/locales that choke on long Unicode paths
        # (e.g. Persian filenames) when opening the final file directly.
        fd, tmp_file = tempfile.mkstemp(dir=".")
        os.close(fd)
        try:
            with requests.get(url, headers=prepare_headers(), stream=True) as r:
                r.raise_for_status()
                with open(tmp_file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            os.replace(tmp_file, output_file)
        finally:
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

    @staticmethod
    def _get_file_format(url):
        return urlparse(url).path.rsplit(".", 1)[-1]
