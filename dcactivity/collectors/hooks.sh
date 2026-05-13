#!/bin/bash

preexec() {
    python -m dcactivity.cli.main --cmd "$1"
}