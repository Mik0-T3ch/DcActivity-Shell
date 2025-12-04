from pypresence import Presence
import time
import os
# Aca se pone el ID de tu discord
CLIENT_ID = "PON_AQUI_TU_CLIENT_ID"
rpc = Presence(CLIENT_ID)
rpc.connect()

while True:
    current_dir = os.getenv("CURRENT_SHELL_DIR", "Desconocida")
    last_cmd = os.getenv("LAST_SHELL_CMD", "")
    user = os.getenv("USER", "")
    
    # ----- LÓGICA DE ESTADOS -----

    #  NANO
    if "nano" in last_cmd:
        large_image = "nano"
        details = "Programando con Nano"
        state = last_cmd

    #  ROOT
    elif user == "root":
        large_image = "superusuario"
        details = "Usando modo root"
        state = last_cmd

    #  SHELL
    else:
        large_image = "terminal"
        details = f"Carpeta: {current_dir}"
        state = last_cmd

    # Actualizar estado
    rpc.update(
        details=details,
        state=state,
        large_image=large_image
    )

    time.sleep(3)

