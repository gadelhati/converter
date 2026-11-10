from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import HTMLResponse, StreamingResponse

from app.services.archive import create_archive
from app.services.converter import convert_rtf

router = APIRouter()


def _check_rtf(filename: str | None) -> None:
    if not (filename or "").lower().endswith(".rtf"):
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo não é RTF: {filename}",
        )


@router.post(
    "/api/convert/html",
    response_class=HTMLResponse,
)
async def convert_one(
    file: UploadFile = File(...),
    revogado: bool = Form(False),
    om: str = Form("DIRETORIA DE HIDROGRAFIA E NAVEGAÇÃO"),
) -> str:
    """Converte um único RTF e devolve o HTML."""

    _check_rtf(file.filename)

    data = await file.read()

    return convert_rtf(
        data,
        revogado=revogado,
        om=om,
    )


@router.post("/api/convert")
async def convert_many(
    files: list[UploadFile] = File(...),
    revogado: bool = Form(False),
    om: str = Form("DIRETORIA DE HIDROGRAFIA E NAVEGAÇÃO"),
):
    """Converte múltiplos RTF e devolve um ZIP."""

    documents = []

    for file in files:
        _check_rtf(file.filename)

        html = convert_rtf(
            await file.read(),
            revogado=revogado,
            om=om,
        )

        filename = Path(file.filename).stem + ".html"

        documents.append((filename, html))

    archive = create_archive(documents)

    return StreamingResponse(
        archive,
        media_type="application/zip",
        headers={"Content-Disposition": ('attachment; filename="portarias_html.zip"')},
    )
