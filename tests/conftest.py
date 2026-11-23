from unittest.mock import MagicMock, patch

import pytest

FAKE_VIDEO = {
    "data": {
        "attributes": {
            "title": "My Video Title",
            "file_link_all": [
                {"profile": "480p", "urls": ["https://link-to-video/a.mp4"]},
                {"profile": "720p", "urls": ["https://link-to-video/b.mp4"]},
                {"profile": "1080p", "urls": ["https://link-to-video/c.mp4"]},
            ],
        }
    }
}


@pytest.fixture(autouse=True)
def no_network():
    """Never hit aparat.com from tests: every requests.get returns FAKE_VIDEO."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(json=MagicMock(return_value=FAKE_VIDEO))
        yield mock_get
