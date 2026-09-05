"""Application-scene images embedded in the 2024 technical catalogue.

The catalogue still labels the magnetic range as ``MAGNETAR``.  Product names
in Verona's database use the replacement brand name ``MAGNETO``; the mapping
below deliberately bridges those names without changing the public product
slugs (which would break existing URLs).
"""

from __future__ import annotations

from pathlib import Path


CATALOG_APPLICATION_PAGE_BY_SLUG = {
    # Magneto Large (MAGNETAR in the source catalogue)
    "magnetar-large-ressed-track-trimless": 14,
    "magnetar-large-surface-pendant-track": 16,
    "magnetar-large-linear": 18,
    "magnetar-large-dot-linear": 20,
    "magnetar-rotate-linear": 22,
    "magnetar-rotate-dot-linear": 24,
    "magnetar-large-angle-linear": 26,
    "magnetar-large-angle-dot-linear": 28,
    "magnetar-large-pendant-35": 30,
    "magnetar-large-pendant-65": 32,
    "magnetar-large-spot-35": 34,
    "magnetar-large-spot-65": 36,
    "magnetar-large-tube-plaxi": 38,
    "magnetar-large-spot-linear": 40,
    "magnetar-large-spot-dot-panel": 42,
    "magnetar-large-spot-panel": 44,
    "magnetar-large-flexible-linear": 46,
    # Magneto Small (MAGNETAR MINI in the source catalogue)
    "magnetar-small-ressed-track-trimles": 48,
    "magnetar-small-surface-pendant-track": 50,
    "magnetar-smll-ressed-track-trim": 52,
    "magnetar-smll-surface-pendant-track": 54,
    "magnetar-small-linear": 56,
    "magnetar-small-dot-linear": 58,
    "magnetar-small-rotate-linear": 60,
    "magnetar-small-spot-35-1": 62,
    "magnetar-small-spot-55": 64,
    "magnetar-smallrotate-dot-linear": 66,
    "magnetar-small-angle-linear": 68,
    "magnetar-small-angle-dot-linear": 70,
    "magnetar-small-pendant-35": 72,
    "magnetar-small-pendant-65": 74,
    "magnetar-small-flexible-linear": 76,
    # SP is the current database name for the SEPEHR catalogue range.
    "sp-mini": 80,
    "sp-narrow": 82,
    "sp-mid-slim": 84,
    "sp-wid": 86,
    "sp-wid-ip": 88,
    "sp-plus": 90,
    "sp-narrow-dot": 92,
    # BD and MD are the current database names for BARDIA and MIRDAMAD.
    "bd-mini": 112,
    "bd-narrow": 114,
    "mirdamad-mini-pendant": 100,
    "md-mini-surface": 100,
    "md-narrow-surface": 102,
    "md-narrow-pendant": 102,
    "md-narrow-dot-pendant": 102,
    "md-narrow-dot-surface": 102,
    "md-mid-surface": 104,
    "md-mid-pendant": 104,
    "mad-old": 108,
    "mad-old-pendant": 108,
    # Panels and downlights.
    "peransa": 138,
    "ring-line-downlight": 140,
    "ring-line-inside": 142,
    "ring-line-inside-90cm": 142,
    "bahar-single": 156,
    "bahar-dual": 158,
    "bahar-triple": 160,
    "payam-6": 162,
    "payam-8": 164,
    "payam-square": 166,
    "payam-led": 168,
    "trimless-4": 170,
    "trimless-8": 172,
    "taban-single": 174,
    "taban-double": 176,
    # Renamed decorative and industrial products.
    "hely-short-diamond": 192,
    "hely-small": 194,
    "hely-mid": 196,
    "hely-angle": 198,
    "arin": 200,
    "liber-large": 202,
    "liber-small": 204,
    "bambo-wall": 232,
    "triton": 242,
    "karen-highbay": 244,
    "moon": 258,
    "roshana": 284,
    # Current 1PH/3PH names for the catalogue's GLOBAL TRACK products.
    "3ph-track-recessed": 178,
    "1ph-track-surface-pendant": 180,
    "3ph-track-surface": 180,
    "1ph-spot": 182,
    "1ph-track-spot-65-p": 184,
    "3ph-spotlight-and-pendant-light": 184,
    "1ph-track-pendant-65": 188,
}


def catalog_application_asset_name(page_number: int) -> str:
    return f"products/catalog_applications/catalog_application_page_{page_number:03d}.jpg"


def _application_image(page):
    """Return the single large image placed in the lower half of an intro page."""
    candidates = [
        image
        for image in page.images
        if image.get("top", 0) > 300
        and image.get("width", 0) > 100
        and image.get("height", 0) > 80
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one lower application image on PDF page {page.page_number}; "
            f"found {len(candidates)}."
        )
    return candidates[0]


def extract_catalog_application_images(pdf_path, media_root, *, overwrite=False):
    """Extract mapped application scenes at their original embedded quality."""
    try:
        import pdfplumber
        from PIL import Image
    except ImportError as exc:  # Only the offline extraction command needs these.
        raise RuntimeError(
            "PDF extraction requires pdfplumber and Pillow in the active Python environment."
        ) from exc

    pdf_path = Path(pdf_path)
    media_root = Path(media_root)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Catalogue PDF not found: {pdf_path}")

    extracted = []
    skipped = []
    unique_pages = sorted(set(CATALOG_APPLICATION_PAGE_BY_SLUG.values()))
    with pdfplumber.open(pdf_path) as document:
        for page_number in unique_pages:
            if page_number > len(document.pages):
                raise ValueError(
                    f"Catalogue has {len(document.pages)} pages; page {page_number} is missing."
                )

            relative_name = catalog_application_asset_name(page_number)
            destination = media_root / relative_name
            if destination.exists() and not overwrite:
                skipped.append(relative_name)
                continue

            image = _application_image(document.pages[page_number - 1])
            image_bytes = image["stream"].get_data()
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary_destination = destination.with_suffix(".tmp")
            try:
                temporary_destination.write_bytes(image_bytes)

                # Pillow verifies that the decoded PDF stream is a complete image.
                with Image.open(temporary_destination) as extracted_image:
                    if extracted_image.format != "JPEG":
                        raise ValueError(
                            f"Expected a JPEG stream on PDF page {page_number}; "
                            f"found {extracted_image.format or 'an unknown format'}."
                        )
                    extracted_image.verify()
                temporary_destination.replace(destination)
            finally:
                temporary_destination.unlink(missing_ok=True)
            extracted.append(relative_name)

    return extracted, skipped
