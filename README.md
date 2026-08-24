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

El objetivo es proporcionar una **presencia dinámica, técnica y contextual** que represente tu flujo de trabajo (editores de código, control de versiones, contenedores, pentesting, gestores de paquetes y herramientas del sistema).

---

# Características principales

- **Detección automática de distribuciones Linux**  
  Identifica distribuciones como Arch Linux, Debian, Ubuntu, Fedora, Kali, Manjaro, openSUSE, Alpine, Void, NixOS, entre otras.

- **Soporte multi-shell**  
  Hooks nativos y no intrusivos para **Bash**, **Zsh** y **Fish**.

- **Control de versiones con Git**  
  Detecta nombre del repositorio, rama activa y comandos (`commit`, `push`, `pull`, `checkout`, `merge`, `rebase`, `clone`, `status`...).

- **Gestores de paquetes**  
  Detección contextual de operaciones en `pacman`, `yay`, `paru`, `apt`, `dnf`, `zypper`, `apk`, `nix`, `flatpak`, `snap`, `cargo`, `npm`, `pnpm`, `bun` y `pip`.

- **Entornos de desarrollo y DevOps**  
  Reconoce comandos de `docker`, `docker compose`, `kubectl`, `helm`, `terraform`, `ansible`, `gcc`, `make`, `go`, `python` y suites de tests (`pytest`).

- **Ciberseguridad y Pentesting**  
  Identifica herramientas como `nmap`, `wireshark`, `burpsuite`, `sqlmap`, `hydra`, `metasploit`, `aircrack-ng`, `ghidra` y fuzzers web.

- **Multiplexores y Hardware**  
  Soporte para `tmux`, `zellij`, `screen`, `nvidia-smi`, `nvtop`, `sensors` e información del sistema.

- **Editores de texto y terminal**  
  Identifica si estás editando archivos con `Neovim`, `Vim`, `Nano`, `Micro`, `Helix`, `Emacs` o `VS Code`.

- **Detección de estado Idle / Inactividad**  
  Cambia automáticamente el estado a inactivo tras un tiempo configurable.

---

# Comandos CLI (`dcactivity`)

Una vez instalado, dispones del comando global `dcactivity`:

```bash
# Iniciar daemon en segundo plano
dcactivity start

# Ver estado del daemon y conexión
dcactivity status

# Probar cómo se verá cualquier comando en Discord
dcactivity test "docker compose up -d"

# Ver configuración activa
dcactivity config

# Detener daemon
dcactivity stop
```

---

# Instalación

### Opción 1: Instalador interactivo
```bash
git clone https://github.com/Mik0-T3ch/DcActivity-Shell.git
cd DcActivity-Shell
chmod +x install.sh
./install.sh
```

### Opción 2: Instalación vía Pip
```bash
git clone https://github.com/Mik0-T3ch/DcActivity-Shell.git
cd DcActivity-Shell
pip install .
```

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

---

# Generación de Assets para Discord

El proyecto incluye un generador de iconos en PNG para todas las distros y herramientas soportadas:

```bash
python3 -m dcactivity.utils.asset_gen
```

Los assets generados en `dcactivity/assets/` pueden subirse directamente a tu aplicación en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications) en la sección **Rich Presence > Art Assets**.

---

# Tests

Ejecutar la suite de pruebas unitarias:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

# Desinstalación

Para remover completamente los hooks y el servicio:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

---

# Licencia

Distribuido bajo la licencia **Apache 2.0**.
