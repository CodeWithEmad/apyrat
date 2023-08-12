"""Console script for apyrat."""
import click

from apyrat.apyrat import Downloader, URLType
from apyrat.utils import get_about_information


def display_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    else:
        ABOUT = get_about_information()
        click.echo(ABOUT["__version__"])
        ctx.exit()


def display_help(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(ctx.get_help())
    ctx.exit()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=display_version,
    expose_value=False,
    is_eager=True,
    help="Show version and exit.",
)
@click.option(
    "-f",
    "--filename",
    type=click.Path(),
    default=None,
    help="Specify the output filename.",
)
@click.option(
    "-q",
    "--quality",
    type=str,
    default=None,
    help="Quality of the video.",
)
@click.option(
    "-y",
    "--confirm",
    is_flag=True,
    default=False,
    help="Use default video quality if not available.",
)
@click.argument("url", type=str, required=True)
@click.pass_context
def main(ctx, url, quality, filename, confirm):
    """
    Download Aparat videos from your terminal
    """
    try:
        downloader = Downloader(url)
    except ValueError:
        click.echo("Invalid URL provided.", err=True)
        ctx.exit(1)

    # set filename if the url type is URLType.VIDEO
    if filename and downloader.url_type == URLType.VIDEO:
        downloader.file_name = filename

    quality_choice = get_quality(downloader, quality, confirm)

    downloader.download(quality_choice)


def get_quality(downloader, quality, confirm):
    if quality and quality not in downloader.qualities:
        click.echo(f"Quality {quality} is not available", err=True)
        if not confirm:
            quality = None

    if not quality:
        quality_choice = click.prompt(
            "Enter the quality you want to download",
            type=click.Choice(downloader._get_available_qualities()),
            default=downloader.default_quality(),
        )
    else:
        quality_choice = quality

    return quality_choice


if __name__ == "__main__":
    main()
