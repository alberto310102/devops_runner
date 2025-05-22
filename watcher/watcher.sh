#!/bin/bash

REPO_URL="https://github.com/alberto310102/Test"
BACKEND_URL="http://mi-api.com/start-pipeline"
LAST_COMMIT_FILE="/home/usuario/git-watcher/last_commit.txt"
SCRIPT_PATH="/home/usuario/git-watcher/git_poll.py"


if [ ! -f "$LAST_COMMIT_FILE" ]; then
    echo "" > "$LAST_COMMIT_FILE"
fi


LAST_COMMIT=$(cat "$LAST_COMMIT_FILE")

NEW_COMMIT=$(python3 "$SCRIPT_PATH" "$REPO_URL" "$LAST_COMMIT" "$BACKEND_URL")

if [ ! -z "$NEW_COMMIT" ]; then
    echo "$NEW_COMMIT" > "$LAST_COMMIT_FILE"
fi

