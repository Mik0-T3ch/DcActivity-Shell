#!/bin/bash

_dcactivity_send() {
    local cmd="$1"
    [ -z "$cmd" ] && return
    
    [[ "$cmd" == *"dcactivity.cli.main"* ]] && return
    [[ "$cmd" == *"_dcactivity_"* ]] && return

    python3 -m dcactivity.cli.main --cmd "$cmd" --cwd "$PWD" --shell "bash" >/dev/null 2>&1 &
}

if type preexec &>/dev/null; then
    preexec_functions+=(_dcactivity_send)
else
    if [ -z "$_DCACTIVITY_BASH_LOADED" ]; then
        _DCACTIVITY_BASH_LOADED=1
        _dcactivity_prev_cmd=""

        _dcactivity_debug_hook() {
            local current_cmd="$BASH_COMMAND"
            if [ -n "$current_cmd" ] && [ "$current_cmd" != "$_dcactivity_prev_cmd" ]; then
                _dcactivity_prev_cmd="$current_cmd"
                _dcactivity_send "$current_cmd"
            fi
        }

        trap '_dcactivity_debug_hook' DEBUG
    fi
fi
