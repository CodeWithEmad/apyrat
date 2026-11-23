import hashlib
import os
from unittest.mock import MagicMock, patch

from src.apyrat import Downloader, VideoQuality


@patch("requests.get")
def test_get_available_videos_single_video(mock_get):
    mock_get.return_value.json.return_value = {
        "data": {
            "attributes": {
                "title": "My Video Title",
                "file_link_all": [
                    {"profile": "720p", "urls": ["https://link-to-video"]},
                    {"profile": "1080p", "urls": ["https://link-to-video"]},
                ],
            }
        }
    }
    downloader = Downloader("https://www.aparat.com/v/qur3I", "outputfile")
    assert len(downloader.videos) == 1
    assert downloader.qualities == ["720p", "1080p"]
    assert len(downloader.videos[0]) == 2


def test_default_quality():
    downloader = Downloader("https://www.aparat.com/v/qur3I", "outputfile")
    downloader.qualities = ["480p", "720p", "1080p"]
    assert downloader.default_quality() == VideoQuality.HD.value


@patch("os.path.isfile", return_value=True)
@patch("requests.get")
def test_download_when_file_exists(mock_get, mock_isfile):
    mock_response = MagicMock()
    mock_response.iter_content.return_value = [b"chunk"]
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value.__enter__ = MagicMock(return_value=mock_response)
    mock_get.return_value.__exit__ = MagicMock(return_value=False)
    downloader = Downloader("https://www.aparat.com/v/qur3I", "outputfile")
    downloader.videos = [
        [
            {
                "title": "My Video Title",
                "profile": "720p",
                "url": "https://link-to-video",
            }
        ]
    ]
    downloader.qualities = ["720p"]
    # The URL has no extension, so the output file is just "outputfile"
    hex_dig = hashlib.md5("outputfile".encode()).hexdigest()
    output_file = f"{hex_dig}_outputfile"
    try:
        downloader.download("720p")
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
    mock_isfile.assert_called_once()
