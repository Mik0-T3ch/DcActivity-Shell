<div align="center">

# DcActivity-Shell

**Rich Presence de Discord basado en tu actividad real en la terminal de Linux**

Una herramienta ligera que detecta lo que haces en tu terminal y lo refleja automáticamente en tu estado de Discord.

<br>

<p>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,bash,linux,discord,git,github&perline=6" />
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Plataforma-Linux-black?style=for-the-badge&logo=linux">
  <img src="https://img.shields.io/badge/Lenguaje-Python-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Scripting-Bash-grey?style=for-the-badge&logo=gnubash">
  <img src="https://img.shields.io/badge/Integración-Discord%20RPC-5865F2?style=for-the-badge&logo=discord">
</p>

</div>

---

# Descripción

**DcActivity-Shell** es una herramienta diseñada para usuarios de Linux que desean que su **Discord Rich Presence refleje su actividad real dentro de la terminal**.

El sistema monitorea eventos relevantes del entorno de shell y actualiza automáticamente el estado en Discord con información contextual como comandos ejecutados, directorios activos o el uso de editores de texto.

El objetivo del proyecto es proporcionar una **presencia dinámica, técnica y automatizada** que represente de forma más auténtica el flujo de trabajo de un usuario en la terminal.

---

# Características

- **Detección del directorio actual**  
  Muestra en Discord la ubicación en la que estás trabajando dentro del sistema.

- **Registro de comandos ejecutados**  
  Refleja actividad relevante dentro de la terminal.

- **Detección de editores de texto**  
  Identifica cuando se están editando archivos usando herramientas como `nano`.

- **Reconocimiento de privilegios elevados**  
  Detecta cuando se ejecutan comandos con `sudo` o en modo root.

- **Integración automática con la terminal**  
  Una vez instalado, el sistema funciona sin intervención manual.

- **Ligero y eficiente**  
  Diseñado para ejecutarse sin afectar el rendimiento del sistema.

---

# Funcionamiento

El sistema funciona monitoreando la actividad del entorno de shell y procesando los eventos relevantes para enviarlos a Discord mediante Rich Presence.

```
Terminal Linux
     │
     │ Monitoreo de actividad
     ▼
Procesamiento con Python
     │
     │ Actualización de presencia
     ▼
Discord Rich Presence
```

Esto permite que Discord muestre información contextual basada en lo que el usuario está haciendo en la terminal.

---

# Requisitos

Antes de instalar el proyecto es recomendable tener:

- Linux
- Python 3
- Git
- Discord ejecutándose en el sistema

---

# Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Mik0-T3ch/DcActivity-Shell.git
cd DcActivity-Shell
```

### 2. Dar permisos de ejecución

```bash
chmod +x install.sh
```

### 3. Ejecutar el instalador

```bash
./install.sh
```

---

# Uso

Después de la instalación:

1. Reinicia tu terminal.
2. El script comenzará a ejecutarse automáticamente.
3. Discord actualizará tu Rich Presence según tu actividad en la terminal.

No es necesario ejecutar comandos adicionales durante el uso normal.

---

# Casos de uso

Este proyecto está pensado principalmente para:

- usuarios de Linux
- desarrolladores
- administradores de sistemas
- entusiastas de la terminal
- personas que desean personalizar su presencia en Discord

---

# Estructura del proyecto

```
DcActivity-Shell
│
├── src/
├── bash/
├── assets/
├── install.sh
├── requirements.txt
└── README.md
```

---

# Autor

**El gatito miau miau :3**

GitHub  
https://github.com/Mik0-T3ch

---

# Licencia

Este proyecto está distribuido bajo la licencia **Apache 2.0**.
