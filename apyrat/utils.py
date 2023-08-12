"""Initialization script."""

import io
import os
from typing import Dict


CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def get_about_information() -> Dict[str, str]:
    about_information: Dict[str, str] = {}
    with io.open(
        os.path.join(CURRENT_DIRECTORY, "__about__.py"), "rt", encoding="utf-8"
    ) as file:
        exec(file.read(), about_information)  # pylint: disable=exec-used
    return about_information


def check_domain_validity(domain: str) -> bool:
    if domain.startswith("https://"):
        domain = domain[8:]
    if domain.startswith("www."):
        domain = domain[4:]

    return domain.startswith("aparat.com/v/") or domain.startswith(
        "aparat.com/playlist/"
    )


def prepare_headers():
    return {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"  # noqa
    }
