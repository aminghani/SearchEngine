#!/bin/bash

RUN_DIR=$(pwd)

DIR=$RUN_DIR"/SearchEngine/data/images"

if [ ! -d "$DIR" ]; then
  echo "Directory does not exist. Creating directory..."
  mkdir -p "$DIR"
  if [ $? -eq 0 ]; then
    echo "Directory created successfully."
  else
    echo "Failed to create directory."
    exit 1
  fi
fi

if [ -z "$(ls -A "$DIR")" ]; then
  echo "Directory is empty. running populate"
  POPULATE_SCRIPT=$RUN_DIR"/SearchEngine/database/populate.sh"

  "$POPULATE_SCRIPT"
  echo "populate is done."
else
  source $RUN_DIR/venv/bin/activate
  echo "running the server."
  python3 $RUN_DIR"/SearchEngine/api/main.py"
fi