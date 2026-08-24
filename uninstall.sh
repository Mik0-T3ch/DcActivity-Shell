#!/bin/bash

echo ">>> Desinstalando DcActivity-Shell..."

if command -v systemctl >/dev/null 2>&1; then
    systemctl --user stop dcactivity 2>/dev/null || true
    systemctl --user disable dcactivity 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/dcactivity.service"
    systemctl --user daemon-reload 2>/dev/null || true
    echo " - Servicio systemd eliminado"
fi

pkill -f "dcactivity.daemon.server" 2>/dev/null || true

if [ -f "$HOME/.bashrc" ]; then
    sed -i '/DcActivity/d' "$HOME/.bashrc"
    sed -i '/dcactivity/d' "$HOME/.bashrc"
    echo " - Hooks eliminados de ~/.bashrc"
fi

if [ -f "$HOME/.zshrc" ]; then
    sed -i '/DcActivity/d' "$HOME/.zshrc"
    sed -i '/dcactivity/d' "$HOME/.zshrc"
    echo " - Hooks eliminados de ~/.zshrc"
fi

FISH_FILE="$HOME/.config/fish/config.fish"
if [ -f "$FISH_FILE" ]; then
    sed -i '/DcActivity/d' "$FISH_FILE"
    sed -i '/dcactivity/d' "$FISH_FILE"
    echo " - Hooks eliminados de config.fish"
fi

echo ">>> Desinstalacion completada."
