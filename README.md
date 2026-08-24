<div align="center">

# DcActivity-Shell

**Rich Presence de Discord basado en tu actividad real en la terminal de Linux**

Una herramienta ligera y modular que detecta lo que haces en tu shell y lo refleja en tiempo real en tu estado de Discord.

<br>

<p>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,bash,linux,discord,git,github,docker,rust&perline=8" />
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Plataforma-Linux-black?style=for-the-badge&logo=linux">
  <img src="https://img.shields.io/badge/Lenguaje-Python-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Shells-Bash%20|%20Zsh%20|%20Fish-grey?style=for-the-badge&logo=gnubash">
  <img src="https://img.shields.io/badge/Integración-Discord%20RPC-5865F2?style=for-the-badge&logo=discord">
</p>

</div>

---

# Descripción

**DcActivity-Shell** es un daemon ligero para Linux que monitoriza la actividad de tu shell favorita (**Bash**, **Zsh** o **Fish**) y la envía como Rich Presence a Discord mediante comunicación IPC/Sockets de baja latencia.

El objetivo es proporcionar una **presencia dinámica, técnica y contextual** que represente tu flujo de trabajo (editores de código, control de versiones, contenedores, gestores de paquetes y herramientas del sistema).

---

# Características principales

- **Detección automática de distribuciones Linux**  
  Identifica distribuciones como Arch Linux, Debian, Ubuntu, Fedora, Kali, Manjaro, openSUSE, Alpine, Void, NixOS, entre otras.

- **Soporte multi-shell**  
  Hooks nativos y no intrusivos para **Bash**, **Zsh** y **Fish**.

- **Gestores de paquetes**  
  Detección contextual de operaciones en `pacman`, `yay`, `paru`, `apt`, `dnf`, `zypper`, `apk`, `nix`, `flatpak`, `snap`, `cargo`, `npm`, `pnpm`, `bun` y `pip`.

- **Entornos de desarrollo y DevOps**  
  Reconoce comandos de `docker`, `docker compose`, `kubectl`, `helm`, `terraform`, `ansible`, `gcc`, `make`, `go`, `python` y suites de tests (`pytest`).

- **Control de versiones con Git**  
  Detecta acciones como `commit`, `push`, `pull`, `checkout`, `merge`, `rebase`, `clone`, `status`, etc.

- **Editores de texto y terminal**  
  Identifica si estás editando archivos con `Neovim`, `Vim`, `Nano`, `Micro`, `Helix`, `Emacs` o `VS Code`.

- **Detección de estado Idle / Inactividad**  
  Cambia automáticamente el estado a inactivo si no se ejecutan comandos tras un tiempo configurable.

- **Modo Privacidad y Personalización**  
  Oculta nombres de archivos o comandos específicos mediante configuración en JSON.

- **Servicio Systemd de usuario**  
  Ejecución en segundo plano sin ralentizar el inicio de sesión.

---

# Arquitectura

```
  ┌─────────────────────────────────────────────────┐
  │         Terminal (Bash / Zsh / Fish)            │
  └────────────────────────┬────────────────────────┘
                           │ (Hook asíncrono)
                           ▼
  ┌─────────────────────────────────────────────────┐
  │           dcactivity.cli.main (JSON)            │
  └────────────────────────┬────────────────────────┘
                           │ (Socket IPC 127.0.0.1:4545)
                           ▼
  ┌─────────────────────────────────────────────────┐
  │          dcactivity.daemon (Engine)             │
  │    ├─ Detectores (Distro, Git, Dev, PKG, etc.)  │
  │    ├─ Temporizador de Inactividad (Idle)        │
  │    └─ Discord RPC (pypresence)                  │
  └────────────────────────┬────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────┐
  │               Discord Rich Presence             │
  └─────────────────────────────────────────────────┘
```

---

# Requisitos

- Linux (cualquier distribución)
- Python 3.8+
- Discord (App nativa o cliente Flatpak/Snap)

---

# Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Mik0-T3ch/DcActivity-Shell.git
cd DcActivity-Shell
```

### 2. Ejecutar el instalador automático
```bash
chmod +x install.sh
./install.sh
```

El script configurará:
- Las dependencias de Python
- Los hooks para tus shells instaladas (`~/.bashrc`, `~/.zshrc` o `~/.config/fish/config.fish`)
- El servicio en segundo plano de Systemd (`systemctl --user enable --now dcactivity`)

---

# Configuración

Puedes personalizar el comportamiento en `~/.config/dcactivity/config.json`:

```json
{
  "client_id": "1446336643320647720",
  "privacy_mode": false,
  "show_current_dir": true,
  "show_distro": true,
  "idle_timeout": 180,
  "idle_text": "Inactivo en terminal",
  "ignored_commands": [
    "clear",
    "history",
    "exit"
  ],
  "update_interval": 2
}
```

### Opciones disponibles:
- `client_id`: ID de la aplicación de Discord (puedes usar la tuya si deseas cambiar las imágenes).
- `privacy_mode`: Oculta el comando/archivo y solo muestra "Trabajando en terminal".
- `show_current_dir`: Muestra el directorio actual (`📁 ~/mi-proyecto`).
- `idle_timeout`: Segundos de inactividad antes de cambiar a estado Idle (`0` para desactivar).
- `ignored_commands`: Lista de comandos que no alteran el estado de Discord.

---

# Generación de Assets para Discord

El proyecto incluye un generador puro de iconos en PNG para todas las distros y herramientas soportadas:

```bash
python3 -m dcactivity.utils.asset_gen
```

Los assets generados en `dcactivity/assets/` pueden subirse directamente a tu aplicación en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications) en la sección **Rich Presence > Art Assets**.

---

# Desinstalación

Para remover completamente los hooks y el servicio:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

---

# Estructura del proyecto

```
DcActivity-Shell
│
├── dcactivity/
│   ├── assets/              # Iconos e imágenes para Rich Presence
│   ├── cli/                 # Cliente CLI ligero para los hooks
│   ├── collectors/          # Hooks para Bash, Zsh y Fish
│   ├── config/              # Configuración predeterminada
│   ├── core/                # Motor central, State, Config y RPC
│   ├── daemon/              # Servidor daemon TCP / IPC
│   ├── detectors/           # Módulos de detección (distro, git, dev, pkg...)
│   └── utils/               # Utilidades y generador de assets
│
├── dcactivity.service       # Unidad Systemd de usuario
├── install.sh               # Instalador interactivo
├── uninstall.sh             # Desinstalador limpio
├── requirements.txt         # Dependencias de Python
└── README.md
```

---

# Licencia

Distribuido bajo la licencia **Apache 2.0**.
