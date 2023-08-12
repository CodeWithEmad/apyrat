from apyrat.apyrat import Downloader
from apyrat.cli import get_quality, main
from unittest.mock import patch
from click.testing import CliRunner


def test_main_download_video_with_quality():
    runner = CliRunner()
    with patch(
        "apyrat.apyrat.Downloader._get_available_qualities",
        return_value=["480", "720", "1080"],
    ) as mock_qualities:
        result = runner.invoke(
            main, ["https://www.aparat.com/v/qur3I", "-q", "720"]
        )
    assert result.exit_code == 0
    mock_qualities.assert_called_once()


def test_main_download_video_without_quality():
    runner = CliRunner()
    with patch(
        "apyrat.apyrat.Downloader._get_available_qualities",
        return_value=["480", "720", "1080"],
    ), patch("click.prompt", return_value="720"):
        result = runner.invoke(main, ["https://www.aparat.com/v/qur3I"])
    assert result.exit_code == 0


def test_get_quality_available():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="720"):
        assert get_quality(downloader, "720", True) == "720"


def test_get_quality_not_available():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="720"):
        assert get_quality(downloader, "240", False) == "720"


def test_get_quality_not_available_no_confirm():
    downloader = Downloader("https://www.aparat.com/v/qur3I")
    downloader.qualities = ["480", "720", "1080"]
    with patch("click.prompt", return_value="480"):
        assert get_quality(downloader, "240", False) == "480"
