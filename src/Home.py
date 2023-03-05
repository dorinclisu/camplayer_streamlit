import os
from configparser import ConfigParser

import streamlit as st

from common import *



config = load()

st.header('Raspberry PI CamPlayer')
st.markdown("""Configuration web interface for camplayer,
    make sure you have it installed already: https://github.com/raspicamplayer/camplayer""")

config.ini_path = st.text_input('Config INI Path', config.ini_path).strip()
config.ini_path = os.path.expanduser(config.ini_path)

if not os.path.isfile(config.ini_path):
    st.error(f'File "{config.ini_path}" does not exist!')
else:
    ini = ConfigParser()
    logging.info(f'Reading camplayer config from "{config.ini_path}"')
    ini.read(config.ini_path)

    ini_content_masked = generate_camplayer_ini(config, ini, masked=True)

    if st.button('🔁 Update'):
        save(config)
        generate_camplayer_ini(config, ini)

        logging.info(f'Writing camplayer config to "{config.ini_path}"')
        with open(config.ini_path, 'w') as f:
            ini.write(f)

        if restart_camplayer():
            st.markdown(':green[Updated]')
        else:
            st.error('Failed to restart camplayer')

    st.code(ini_content_masked)
