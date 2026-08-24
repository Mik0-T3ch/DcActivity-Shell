# DcActivity Hook para Fish Shell

function _dcactivity_fish_preexec --on-event fish_preexec
    set -l cmd $argv[1]
    test -z "$cmd"; and return

    # Evitar llamadas recursivas
    string match -q "*dcactivity.cli.main*" "$cmd"; and return
    string match -q "*_dcactivity_*" "$cmd"; and return

    python3 -m dcactivity.cli.main --cmd "$cmd" --cwd "$PWD" --shell "fish" >/dev/null 2>&1 &
end
