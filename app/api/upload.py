from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.dataset_validation import validate_dataset


router = APIRouter()

# Project root: HCL_Training/
BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed formats: CSV, XLSX, JSON."
            ),
        )

    dataset_id = str(uuid4())
    destination = UPLOAD_DIR / f"{dataset_id}{extension}"

    total_size = 0

    try:
        with destination.open("wb") as output_file:
            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds the 100 MB size limit.",
                    )

                output_file.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # Validate actual dataset contents.
        validation = validate_dataset(str(destination))

    except HTTPException:
        destination.unlink(missing_ok=True)
        raise

    except (FileNotFoundError, ValueError) as exc:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Dataset upload failed.",
        ) from exc

    finally:
        await file.close()

    return {
        "dataset_id": str(destination),
        "filename": file.filename,
        "size_bytes": total_size,
        "extension": extension,
        "validation": validation,
    }