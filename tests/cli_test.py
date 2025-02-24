from unittest.mock import patch

from click.testing import CliRunner

from src.apyrat import Downloader
from src.cli import get_quality, main


def test_main_download_video_with_quality():
    runner = CliRunner()
    with patch(
        "src.apyrat.Downloader._get_available_qualities",
        return_value=["480", "720", "1080"],
    ) as mock_qualities, patch(
        "src.apyrat.Downloader.download",
        return_value=None,
    ) as mock_download:
        result = runner.invoke(
            main,
            [
                "https://www.aparat.com/v/qur3I",
                "-q",
                "720",
            ],
        )
    assert result.exit_code == 0
    mock_qualities.assert_called_once()
    mock_download.assert_called_once_with("720")


def test_main_download_video_without_quality():
    runner = CliRunner()
    with patch(
        "src.apyrat.Downloader._get_available_qualities",
        return_value=["480", "720", "1080"],
    ), patch("click.prompt", return_value="720"):
        result = runner.invoke(main, ["https://www.aparat.com/v/qur3I"])
    assert result.exit_code == 0


def test_get_quality_available():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="720"):
        assert get_quality(downloader, "720") == "720"


def test_get_quality_not_available():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="720"):
        assert get_quality(downloader, "240") == "720"


def test_get_quality_not_available_no_confirm():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="480"):
        assert get_quality(downloader, "240") == "480"
