#!/bin/bash

RUN_DIR=$(pwd)

DIR=$RUN_DIR"/SearchEngine/data/images"

if [ ! -d "$DIR" ]; then
  echo "Directory does not exist."
  exit 1
fi

if [ -z "$(ls -A "$DIR")" ]; then
  echo "Directory is empty. running populate"
  POPULATE_SCRIPT=$RUN_DIR"/SearchEngine/database/populate.sh"

  "$POPULATE_SCRIPT"
  echo "populate is done."
else
  echo "running the server."
  python3 $RUN_DIR"/SearchEngine/api/main.py"
fi