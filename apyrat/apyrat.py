import hashlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
from urllib.parse import urlparse

import click
import requests
import wget

from apyrat.utils import prepare_headers, check_domain_validity


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
        url = url.lstrip("https://").lstrip("www.").rstrip("/")
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
                if item["type"] == "Video"
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
        qualities = set(
            video_quality.get("profile")
            for video in self.videos
            for video_quality in video
        )
        return sorted(qualities, key=lambda x: int(x[:-1]))

    def default_quality(self):
        return (
            VideoQuality.HD.value
            if VideoQuality.HD.value in self.qualities
            else self.qualities[-1]
        )

    def download(self, quality: str):
        for video in self.videos:
            for item in video:
                if item.get("profile") == quality:
                    url = item.get("url")
                    title = item.get("title")
                    click.echo(f"{title}\n{url}")
                    file_name = self.file_name or item.get("title")
                    output_file = f"{file_name}.{self._get_file_format(url)}"
                    # Check if file already exists
                    if os.path.isfile(output_file):
                        # Create a hash of the filename
                        hash_object = hashlib.md5(output_file.encode())
                        hex_dig = hash_object.hexdigest()
                        # Append the hash to the filename
                        output_file = f"{hex_dig}{output_file}"
                    wget.download(url, out=output_file)

    @staticmethod
    def _get_file_format(url):
        return urlparse(url).path.rsplit(".", 1)[-1]
