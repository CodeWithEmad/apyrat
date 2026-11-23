<div align="center">

<img src="assets/logo.png" alt="Apyrat" width="240">

# Apyrat

**Download [Aparat](https://www.aparat.com) videos and playlists from your terminal.**

[![PyPI](https://img.shields.io/pypi/v/apyrat?logo=pypi&logoColor=white)](https://pypi.org/project/apyrat/)
[![Python](https://img.shields.io/pypi/pyversions/apyrat?logo=python&logoColor=white)](https://pypi.org/project/apyrat/)
[![Tests](https://img.shields.io/github/actions/workflow/status/CodeWithEmad/apyrat/test.yml?branch=master&label=tests)](https://github.com/CodeWithEmad/apyrat/actions/workflows/test.yml)
[![Downloads](https://static.pepy.tech/badge/apyrat)](https://pepy.tech/projects/apyrat)
[![License](https://img.shields.io/github/license/CodeWithEmad/apyrat)](https://github.com/CodeWithEmad/apyrat/blob/master/LICENSE)

![Monthly downloads](https://raw.githubusercontent.com/CodeWithEmad/apyrat/master/.pypi_chart/badge.svg)

</div>

## Install

```bash
pipx install apyrat        # recommended: isolated, always on your PATH
# or
uv tool install apyrat
# or
pip install -U apyrat
```

Requires Python 3.10+.

## Usage

```bash
# a single video: pick a quality interactively
apyrat https://www.aparat.com/v/qur3I

# skip the prompt: 720p, or the best available if missing
apyrat -y https://www.aparat.com/v/qur3I

# an exact quality, with your own filename
apyrat -q 1080p -f lecture https://www.aparat.com/v/qur3I

# a whole playlist, in playlist order
apyrat -y https://www.aparat.com/playlist/448747
```

### Options

| Option | Description |
| --- | --- |
| `-q, --quality` | Quality to download, e.g. `480p`, `720p`, `1080p`. Prompts if it isn't available. |
| `-y, --confirm` | Don't prompt: use 720p, or the highest available quality if 720p is missing. |
| `-f, --filename` | Output filename (single videos only; the extension is added for you). |
| `-v, --version` | Show the version and exit. |
| `-h, --help` | Show help and exit. |

### Good to know

- Files are saved in the current directory, named after the video title. Persian
  titles work; characters that filesystems reject are removed.
- If a file with the same name already exists, a short hash is prefixed to the
  new one instead of overwriting it.
- Supported links: `aparat.com/v/<id>` and `aparat.com/playlist/<id>`.

## Contributing

Bug reports and pull requests are welcome. See [CONTRIBUTING.md](https://github.com/CodeWithEmad/apyrat/blob/master/CONTRIBUTING.md)
for the dev setup (`make install`, `make test`) and the release process.

## License

[MIT](https://github.com/CodeWithEmad/apyrat/blob/master/LICENSE)
