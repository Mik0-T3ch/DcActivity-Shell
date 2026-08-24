import os
import platform
import re


DISTRO_ASSET_MAP = {
    "arch": "arch",
    "artix": "arch",
    "manjaro": "manjaro",
    "endeavouros": "arch",
    "ubuntu": "ubuntu",
    "pop": "pop_os",
    "mint": "linuxmint",
    "linuxmint": "linuxmint",
    "debian": "debian",
    "fedora": "fedora",
    "rhel": "redhat",
    "centos": "centos",
    "almalinux": "almalinux",
    "rocky": "rocky",
    "opensuse": "opensuse",
    "opensuse-tumbleweed": "opensuse",
    "opensuse-leap": "opensuse",
    "gentoo": "gentoo",
    "alpine": "alpine",
    "void": "void",
    "kali": "kali",
    "parrot": "parrot",
    "nixos": "nixos",
    "slackware": "slackware"
}


def parse_os_release():
    paths = ["/etc/os-release", "/usr/lib/os-release"]
    data = {}
    
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            v = v.strip("\"'")
                            data[k.upper()] = v
                break
            except Exception:
                pass
    return data


def get_distro_info():
    os_info = parse_os_release()
    
    distro_id = os_info.get("ID", "").lower()
    distro_id_like = os_info.get("ID_LIKE", "").lower()
    pretty_name = os_info.get("PRETTY_NAME") or os_info.get("NAME")
    
    if not pretty_name:
        sys_name = platform.system()
        if sys_name == "Linux":
            pretty_name = "GNU/Linux"
        else:
            pretty_name = sys_name or "Linux"

    asset_key = DISTRO_ASSET_MAP.get(distro_id)
    if not asset_key and distro_id_like:
        for like_id in distro_id_like.split():
            if like_id in DISTRO_ASSET_MAP:
                asset_key = DISTRO_ASSET_MAP[like_id]
                break

    if not asset_key:
        asset_key = "linux"

    return {
        "id": distro_id or "linux",
        "name": pretty_name,
        "asset_key": asset_key,
        "kernel": platform.release()
    }
