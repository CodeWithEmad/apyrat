from unittest.mock import patch
from apyrat.apyrat import Downloader, VideoQuality


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
@patch("wget.download")
def test_download_when_file_exists(mock_wget, mock_isfile):
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
    downloader.download("720p")
    mock_wget.assert_called_once()
    mock_isfile.assert_called_once()
