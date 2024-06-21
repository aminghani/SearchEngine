CURR_DIR=$(pwd)
CONFIG_FILE=$CURR_DIR"/config.ini"

MASTER_KEY=$(grep -A 1 "\[meili\]" $CONFIG_FILE | grep "master_key" | cut -d '=' -f2 | tr -d ' ')

echo "master_key: $MASTER_KEY"
