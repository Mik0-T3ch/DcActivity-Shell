#!/bin/zsh

_dcactivity_zsh_preexec() {
    local cmd="$1"
    [[ -z "$cmd" ]] && return

    [[ "$cmd" == *"dcactivity.cli.main"* ]] && return
    [[ "$cmd" == *"_dcactivity_"* ]] && return

    python3 -m dcactivity.cli.main --cmd "$cmd" --cwd "$PWD" --shell "zsh" >/dev/null 2>&1 &!
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _dcactivity_zsh_preexec
