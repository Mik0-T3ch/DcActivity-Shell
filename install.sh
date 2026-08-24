#!/bin/bash

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/dcactivity"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo ">>> Instalando DcActivity-Shell desde $REPO_DIR..."

if command -v pip3 >/dev/null 2>&1; then
    echo " - Instalando dependencias de Python..."
    pip3 install -r "$REPO_DIR/requirements.txt" 2>/dev/null || {
        echo "   Intentando con --break-system-packages..."
        pip3 install --break-system-packages -r "$REPO_DIR/requirements.txt" || true
    }
else
    echo "!! Aviso: pip3 no encontrado. Asegurate de instalar pypresence."
fi

mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cp "$REPO_DIR/dcactivity/config/default.json" "$CONFIG_DIR/config.json"
    echo " - Creada configuracion en $CONFIG_DIR/config.json"
fi

chmod +x "$REPO_DIR/dcactivity/collectors/hooks.sh" 2>/dev/null || true
chmod +x "$REPO_DIR/dcactivity/collectors/hooks.zsh" 2>/dev/null || true

if [ -f "$HOME/.bashrc" ]; then
    BASH_HOOK="export PYTHONPATH=\"$REPO_DIR:\$PYTHONPATH\"\nsource \"$REPO_DIR/dcactivity/collectors/hooks.sh\""
    if ! grep -q "dcactivity/collectors/hooks.sh" "$HOME/.bashrc"; then
        echo -e "\n# DcActivity Shell Hook\n$BASH_HOOK" >> "$HOME/.bashrc"
        echo " - Hook anadido a ~/.bashrc"
    fi
fi

if [ -f "$HOME/.zshrc" ]; then
    ZSH_HOOK="export PYTHONPATH=\"$REPO_DIR:\$PYTHONPATH\"\nsource \"$REPO_DIR/dcactivity/collectors/hooks.zsh\""
    if ! grep -q "dcactivity/collectors/hooks.zsh" "$HOME/.zshrc"; then
        echo -e "\n# DcActivity Shell Hook\n$ZSH_HOOK" >> "$HOME/.zshrc"
        echo " - Hook anadido a ~/.zshrc"
    fi
fi

FISH_CONFIG_DIR="$HOME/.config/fish"
if [ -d "$FISH_CONFIG_DIR" ] || command -v fish >/dev/null 2>&1; then
    mkdir -p "$FISH_CONFIG_DIR"
    FISH_HOOK="set -gx PYTHONPATH \"$REPO_DIR:\$PYTHONPATH\"\nsource \"$REPO_DIR/dcactivity/collectors/hooks.fish\""
    FISH_FILE="$FISH_CONFIG_DIR/config.fish"
    touch "$FISH_FILE"
    if ! grep -q "dcactivity/collectors/hooks.fish" "$FISH_FILE"; then
        echo -e "\n# DcActivity Shell Hook\n$FISH_HOOK" >> "$FISH_FILE"
        echo " - Hook anadido a ~/.config/fish/config.fish"
    fi
fi

if command -v systemctl >/dev/null 2>&1; then
    mkdir -p "$SYSTEMD_USER_DIR"
    sed "s|{{REPO_DIR}}|$REPO_DIR|g" "$REPO_DIR/dcactivity.service" > "$SYSTEMD_USER_DIR/dcactivity.service" 2>/dev/null || true
    systemctl --user daemon-reload 2>/dev/null || true
    systemctl --user enable --now dcactivity 2>/dev/null || true
    echo " - Servicio systemd configurado e iniciado (dcactivity.service)"
else
    echo " - Anadiendo auto-inicio a .bashrc (sin systemd)..."
    AUTO_CMD="pgrep -f 'dcactivity.daemon.server' >/dev/null || nohup python3 -m dcactivity.daemon.server >/dev/null 2>&1 &"
    if [ -f "$HOME/.bashrc" ] && ! grep -q "dcactivity.daemon.server" "$HOME/.bashrc"; then
        echo "if [[ \$- == *i* ]]; then $AUTO_CMD; fi" >> "$HOME/.bashrc"
    fi
fi

echo ">>> Instalacion completada exitosamente."
echo "Reinicia tu terminal para comenzar."
