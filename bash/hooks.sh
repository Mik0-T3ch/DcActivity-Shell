#!/bin/bash

EVENT_FILE="$HOME/DcActivity-Shell/event.log"

[ ! -f "$EVENT_FILE" ] && touch "$EVENT_FILE"

_update_dcactivity_log() {

    _cmd=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//')
    [ -z "$_cmd" ] && _cmd="(ninguno)"
    _dir=$(pwd)
    _usr="$USER"
    printf "CMD:%s\nDIR:%s\nUSER:%s\n" \
        "$_cmd" "$_dir" "$_usr" >> "$EVENT_FILE"

}

if [[ -z "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="_update_dcactivity_log"
else
    # unimos lo que ya había con nuestro logger
    PROMPT_COMMAND="${PROMPT_COMMAND}; _update_dcactivity_log"
fi

