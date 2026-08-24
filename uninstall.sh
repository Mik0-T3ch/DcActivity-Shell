#!/bin/bash

echo ">>> Desinstalando DcActivity-Shell..."

# 1. Detener y deshabilitar systemd service
if command -v systemctl >/dev/null 2>&1; then
    systemctl --user stop dcactivity 2>/dev/null || true
    systemctl --user disable dcactivity 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/dcactivity.service"
    systemctl --user daemon-reload 2>/dev/null || true
    echo " - Servicio systemd eliminado"
fi

# 2. Matar procesos activos
pkill -f "dcactivity.daemon.server" 2>/dev/null || true

# 3. Limpiar hooks de .bashrc
if [ -f "$HOME/.bashrc" ]; then
    sed -i '/DcActivity/d' "$HOME/.bashrc"
    sed -i '/dcactivity/d' "$HOME/.bashrc"
    echo " - Hooks eliminados de ~/.bashrc"
fi

# 4. Limpiar hooks de .zshrc
if [ -f "$HOME/.zshrc" ]; then
    sed -i '/DcActivity/d' "$HOME/.zshrc"
    sed -i '/dcactivity/d' "$HOME/.zshrc"
    echo " - Hooks eliminados de ~/.zshrc"
fi

# 5. Limpiar hooks de fish
FISH_FILE="$HOME/.config/fish/config.fish"
if [ -f "$FISH_FILE" ]; then
    sed -i '/DcActivity/d' "$FISH_FILE"
    sed -i '/dcactivity/d' "$FISH_FILE"
    echo " - Hooks eliminados de config.fish"
fi

echo ">>> Desinstalacion completada."
