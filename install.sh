#!/bin/bash
LOCATION="/opt/camplayer_streamlit"

set -e

if [ `whoami` != root ]; then
    echo "Please run with sudo!"
    exit 1
fi

# install system dependencies
apt update
apt install -y --no-install-recommends build-essential cmake python3-dev python3-pip python3-venv
apt install -y --no-install-recommends libatlas-base-dev  # for numpy

# install python dependencies
mkdir -p $LOCATION
python3 -m venv $LOCATION/venv
source $LOCATION/venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-no-deps.txt --no-dependencies

cp -r src/. $LOCATION/
cp camplayer_streamlit /usr/local/bin/
cp camplayer_streamlit.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable camplayer_streamlit
systemctl start camplayer_streamlit
