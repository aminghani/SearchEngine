#!/bin/bash

CURR_DIR=$(pwd)
CONFIG_FILE=$CURR_DIR"/config.ini"

if ! command -v meilisearch &> /dev/null; then
    echo "Meilisearch is not installed. Installing..."
    curl -L https://install.meilisearch.com | sh
else
    echo "Meilisearch is already installed."
fi

MASTER_KEY=$(grep -A 1 "\[meili\]" $CONFIG_FILE | grep "master_key" | cut -d '=' -f2 | tr -d ' ')

echo "master_key: $MASTER_KEY"

./meilisearch --master-key=$MASTER_KEY &

cd $CURR_DIR
