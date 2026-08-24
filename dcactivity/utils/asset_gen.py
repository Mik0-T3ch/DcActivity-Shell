import io
import os
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

OFFICIAL_ICONS = {
    "arch.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/arch-linux.png",
    "ubuntu.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/ubuntu-linux.png",
    "debian.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/debian-linux.png",
    "fedora.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/fedora.png",
    "kali.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/kali-linux.png",
    "manjaro.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/manjaro-linux.png",
    "opensuse.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/opensuse.png",
    "linuxmint.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/linux-mint.png",
    "gentoo.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/gentoo-linux.png",
    "alpine.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/alpine-linux.png",
    "linux.png": "https://raw.githubusercontent.com/marwin1991/profile-technology-icons/main/icons/linux.png",
    "docker.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/docker.png",
    "git.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/git.png",
    "python.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/python.png",
    "rust.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/rust-dark.png",
    "neovim.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/neovim.png",
    "vim.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/vim-dark.png",
    "shell.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/terminal.png",
    "terminal.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/terminal.png",
    "bash.png": "https://raw.githubusercontent.com/marwin1991/profile-technology-icons/main/icons/bash.png",
    "k8s.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/kubernetes.png",
    "package.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/box.png",
    "network.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/wireguard.png",
    "system.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/glances.png",
    "sudo.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/bitwarden.png",
    "c.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/c.png",
    "go.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/go.png",
    "node.png": "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/node-red.png"
}


def create_badge(filename, title, subtitle, accent_color):
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([20, 20, size - 20, size - 20], radius=100, fill=(24, 26, 32, 255), outline=accent_color, width=12)
    draw.ellipse([size // 2 - 130, size // 2 - 130, size // 2 + 130, size // 2 + 130], fill=(accent_color[0], accent_color[1], accent_color[2], 30))

    try:
        font_large = ImageFont.truetype("arial.ttf", 110)
        font_small = ImageFont.truetype("arial.ttf", 46)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    bbox_t = draw.textbbox((0, 0), title, font=font_large)
    w_t = bbox_t[2] - bbox_t[0]
    draw.text(((size - w_t) / 2, 160), title, fill=accent_color, font=font_large)

    bbox_s = draw.textbbox((0, 0), subtitle, font=font_small)
    w_s = bbox_s[2] - bbox_s[0]
    draw.text(((size - w_s) / 2, 310), subtitle, fill=(240, 240, 240, 255), font=font_small)

    img.save(ASSETS_DIR / filename, "PNG")


def download_all_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[ASSETS] Descargando logos oficiales en {ASSETS_DIR}...")
    for filename, url in OFFICIAL_ICONS.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            res = urllib.request.urlopen(req, timeout=10)
            data = res.read()
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            img.save(ASSETS_DIR / filename, "PNG")
            print(f" -> Guardado: {filename}")
        except Exception as e:
            print(f" -> Fallo al descargar {filename}: {e}")

    create_badge("zsh.png", "%_", "Z SH", (243, 156, 18))
    create_badge("fish.png", "><>", "FISH", (0, 206, 201))
    create_badge("nano.png", "^G", "GNU NANO", (78, 170, 37))
    print("[ASSETS] Proceso completado.")


if __name__ == "__main__":
    download_all_assets()
