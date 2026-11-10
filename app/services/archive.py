import io
import zipfile

from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = APP_DIR / "static"

ASSETS = [
    "css/portaria-css.css",
    "css/portarias_html.css",
    "img/brasao.png",
]


def create_archive(
    documents: list[tuple[str, str]],
) -> io.BytesIO:
    """Cria um ZIP contendo HTML e seus respectivos recursos."""

    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as archive:
        for filename, html in documents:
            archive.writestr(filename, html)

        for asset in ASSETS:
            archive.write(
                STATIC_DIR / asset,
                asset,
            )

    buffer.seek(0)

    return buffer
