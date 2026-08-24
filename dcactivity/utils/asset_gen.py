import os
import struct
import zlib
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def create_png(width, height, color_bg, symbol_type="rect", color_fg=(255, 255, 255)):
    raw_data = bytearray()
    
    cx, cy = width / 2.0, height / 2.0
    r_circle = width * 0.38

    for y in range(height):
        raw_data.append(0)
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = (dx * dx + dy * dy) ** 0.5

            if dist <= r_circle:
                raw_data.extend(color_bg)
            else:
                if dist <= r_circle + 4:
                    alpha = int(max(0, min(255, (r_circle + 4 - dist) * 64)))
                    raw_data.extend((color_bg[0], color_bg[1], color_bg[2]))
                else:
                    raw_data.extend((20, 24, 30))

    compressed = zlib.compress(bytes(raw_data), 9)

    png_signature = b"\x89PNG\r\n\x1a\n"

    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = struct.pack(">I", zlib.crc32(b"IHDR" + ihdr_data) & 0xffffffff)
    ihdr = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + ihdr_crc

    idat_crc = struct.pack(">I", zlib.crc32(b"IDAT" + compressed) & 0xffffffff)
    idat = struct.pack(">I", len(compressed)) + b"IDAT" + compressed + idat_crc

    iend_crc = struct.pack(">I", zlib.crc32(b"IEND") & 0xffffffff)
    iend = struct.pack(">I", 0) + b"IEND" + iend_crc

    return png_signature + ihdr + idat + iend


THEMES = {
    "arch": (23, 147, 209),
    "ubuntu": (233, 84, 32),
    "debian": (215, 10, 83),
    "fedora": (41, 65, 114),
    "kali": (85, 124, 191),
    "manjaro": (53, 191, 92),
    "linux": (243, 156, 18),
    "docker": (36, 150, 237),
    "git": (240, 80, 50),
    "python": (55, 118, 171),
    "rust": (222, 165, 132),
    "neovim": (87, 161, 67),
    "vim": (1, 152, 51),
    "package": (155, 89, 182),
    "network": (0, 206, 201),
    "system": (112, 161, 255),
    "bash": (78, 170, 37),
    "zsh": (243, 156, 18),
    "fish": (230, 126, 34)
}


def generate_all_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"[ASSETS] Generando iconos en {ASSETS_DIR}...")
    for name, color in THEMES.items():
        out_path = ASSETS_DIR / f"{name}.png"
        png_bytes = create_png(256, 256, color)
        with open(out_path, "wb") as f:
            f.write(png_bytes)
        print(f" -> Creado: {out_path.name}")
    print("[ASSETS] Generacion completada.")


if __name__ == "__main__":
    generate_all_assets()
