#!/bin/sh
LOCATION="/opt/camplayer_streamlit"

# install dependencies
python -m venv $LOCATION/venv
source $LOCATION/venv/bin/activate
pip install -r requirements.txt

cp -r src/ $LOCATION/
cp camplayer_streamlit /usr/local/bin/
cp camplayer_streamlit.service /etc/systemd/

sudo systemctl daemon-reload
sudo systemctl enable camplayer_streamlit
