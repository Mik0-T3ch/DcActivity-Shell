#!/bin/bash

EVENT_FILE="/home/caponikov/DcActivity-Shell/event.log"
touch "$EVENT_FILE"

update_event_log() {
    # Carpeta actual

    echo "DIR:$(pwd)" >> "$EVENT_FILE"

    # Último comando real de la historia

    last_cmd=$(history 1 | sed 's/^[ ]*[0-9]\+[ ]*//')

    # Registrar comando solo si cambia

    if [ "$last_cmd" != "$LAST_LOGGED_CMD" ]; then
        echo "CMD:$last_cmd" >> "$EVENT_FILE"
        LAST_LOGGED_CMD="$last_cmd"
    fi

    # Usuario

    echo "USER:$(whoami)" >> "$EVENT_FILE"
}

PROMPT_COMMAND=update_event_log

