import mimetypes


def detect_modality(filename: str, content_type: str | None) -> str | None:
    """Return "video", "audio" or "text" from the file name or MIME type, else None."""
    guessed, _ = mimetypes.guess_type(filename)
    for mime in (guessed, content_type):
        if not mime:
            continue
        for modality in ("video", "audio", "text"):
            if mime.startswith(modality + "/"):
                return modality
    return None
