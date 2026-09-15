#!/usr/bin/env bash
# Drops the fixture paper into the case cwd. add_dirs only grants read access at
# the fixture's original path, which the model cannot know; copying keeps the
# prompt honest ("paper.pdf is in this directory").
set -eu
cp "$(dirname "$0")/fixture/paper.pdf" ./paper.pdf
