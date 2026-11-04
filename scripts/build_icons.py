"""Recadre le logo officiel SMKTECH et génère favicon + icônes PWA.

Usage : python3 scripts/build_icons.py <chemin/logo.png>
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
APP = ROOT / "src" / "app"


def trim(img: Image.Image) -> Image.Image:
    """Recadre sur les pixels visibles (le logo officiel a un fond transparent)."""
    img = img.convert("RGBA")
    box = img.getchannel("A").point(lambda p: 255 if p > 10 else 0).getbbox()
    return img.crop(box) if box else img


def square(img: Image.Image, size: int, pad_ratio: float, bg) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), bg)
    inner = int(size * (1 - 2 * pad_ratio))
    im = img.copy()
    im.thumbnail((inner, inner), Image.LANCZOS)
    canvas.alpha_composite(im, ((size - im.width) // 2, (size - im.height) // 2))
    return canvas


def main() -> None:
    src = Image.open(sys.argv[1])
    logo = trim(src)
    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / "icons").mkdir(exist_ok=True)

    logo_web = logo.copy()
    logo_web.thumbnail((512, 512), Image.LANCZOS)
    logo_web.save(PUBLIC / "smktech-logo.png", optimize=True)

    white = (255, 255, 255, 255)
    for size in (192, 512):
        square(logo, size, 0.10, white).save(PUBLIC / "icons" / f"icon-{size}.png", optimize=True)
    square(logo, 512, 0.20, white).save(PUBLIC / "icons" / "maskable-512.png", optimize=True)
    square(logo, 180, 0.10, white).convert("RGB").save(APP / "apple-icon.png", optimize=True)
    square(logo, 64, 0.04, (0, 0, 0, 0)).save(APP / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("logo:", logo.size, "->", logo_web.size)


if __name__ == "__main__":
    main()
