#!/bin/sh
LOCATION="/opt/camplayer_streamlit"

set -e

# install dependencies
python -m venv $LOCATION/venv
source $LOCATION/venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-no-deps.txt --no-dependencies

cp -r src/ $LOCATION/
cp camplayer_streamlit /usr/local/bin/
cp camplayer_streamlit.service /etc/systemd/

sudo systemctl daemon-reload
sudo systemctl enable camplayer_streamlit
