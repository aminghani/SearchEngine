#!/bin/bash

VENV_DIR=$(pwd)
echo $VENV_DIR

if [ ! -d $VENV_DIR"/venv" ]; then
    echo "Virtual environment not found. Creating one..."
    
    apt-get update
    apt install python3.8-venv
    
    python3 -m venv venv
    
    source $VENV_DIR/venv/bin/activate
    
    pip install -r $VENV_DIR/requirements.txt
    
    echo "Virtual environment created and activated."
else
    echo "Virtual environment already exists."
    
    source $VENV_DIR/venv/bin/activate
    
    echo "Virtual environment activated."
fi

python3 SearchEngine/database/populate.py

echo "finished populating."