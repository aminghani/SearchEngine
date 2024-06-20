#!/bin/bash

CURR_DIR=$(pwd)
CONFIG_FILE=$CURR_DIR"/config.ini"

if ! command -v meilisearch &> /dev/null; then
    echo "Meilisearch is not installed. Installing..."
    curl -L https://install.meilisearch.com | sh
else
    echo "Meilisearch is already installed."
fi

MASTER_KEY=$(grep "^master_key=" $CONFIG_FILE | sed 's/master_key=//')

echo "master_key: $MASTER_KEY"

./meilisearch --master-key=key &

cd $CURR_DIR
