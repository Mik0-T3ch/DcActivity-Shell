#!/bin/bash

set -e

REPO_DIR="$HOME/DcActivity-Shell"
BASHRC="$HOME/.bashrc"

echo ">>> Instalando DcActivity-Shell..."

# Crea el event.log si no existe

if [ ! -f "$REPO_DIR/event.log" ]; then
    touch "$REPO_DIR/event.log"
    echo " - Creado event.log"
fi

# Instala las dependencias de Python

if command -v pip3 >/dev/null 2>&1; then
    echo " - Instalando dependencias de Python..."
    pip3 install -r "$REPO_DIR/requirements.txt" || {
        echo "   pip3 normal falló. En Ubuntu 24 puedes usar:"
        echo "   pip3 install --break-system-packages -r requirements.txt"
    }
else
    echo "!! No se encontró pip3. Instálalo con: sudo apt install python3-pip"
fi

# Asegurar el permiso del script

chmod +x "$REPO_DIR/bash/hooks.sh"
chmod +x "$REPO_DIR/src/presence.py"

# Añade el hooks.sh a .bashrc si no está
if ! grep -q "DcActivity-Shell/bash/hooks.sh" "$BASHRC"; then
    echo " - Añadiendo hooks a ~/.bashrc"
    echo "source \"$REPO_DIR/bash/hooks.sh\"" >> "$BASHRC"
fi

# Inicia automaticamente el presence.py solo en shells interactivas

AUTO_LINE='if [[ $- == *i* ]]; then pgrep -f "DcActivity-Shell/src/presence.py" >/dev/null || nohup python3 "$HOME/DcActivity-Shell/src/presence.py" >/dev/null 2>&1 & fi'

if ! grep -q "DcActivity-Shell/src/presence.py" "$BASHRC"; then
    echo " - Configurando auto-inicio de presence.py"
    echo "$AUTO_LINE" >> "$BASHRC"
fi

echo ">>> Instalación completada."
echo "Cierra esta terminal y abre una nueva para que se aplique la configuración."
