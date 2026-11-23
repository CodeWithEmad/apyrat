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
