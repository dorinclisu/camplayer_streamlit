import io
import json
import logging
import os
import subprocess
from configparser import ConfigParser, SectionProxy

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from models import *



logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='{levelname:7} [{filename}:{lineno:03d}]\t {message}',
    style='{',
    force=True,
)
#logging.getLogger().setLevel(os.getenv('LOG_LEVEL', 'INFO'))

config_path = os.getenv('CONFIG_PATH', 'config.json')


def load() -> Config:
    logging.info(f'Loading app config from "{config_path}"')
    try:
        with open(config_path) as f:
            config_raw = json.load(f)
            config = Config(**config_raw)
            return config
    except FileNotFoundError:
        logging.warning('Config file not found, creating default')
        config = Config()
        save(config)
        return config


def save(config: Config):
    logging.info(f'Saving app config to "{config_path}"')
    with open(config_path, 'w') as f:
        config_raw = config.dict(exclude_none=True)
        json.dump(config_raw, f, indent=1)


def setup_stream(stream: ChannelStream, id: str):
    stream.brand = st.selectbox('Brand', DeviceBrand.options(), DeviceBrand.options().index(stream.brand), key=f'brand{id}')  # type: ignore[assignment]
    stream.host = st.text_input('Host', stream.host, key=f'host{id}').strip()
    stream.port = st.number_input('Port', min_value=80, max_value=2**15-1, value=stream.port, step=1, key=f'port{id}')  # type: ignore[assignment]
    stream.ch = st.number_input('Channel', min_value=1, max_value=64, value=stream.ch, step=1, key=f'ch{id}')  # type: ignore[assignment]
    stream.hd = st.checkbox('HD', stream.hd, key=f'hd{id}')
    stream.user = st.text_input('User', stream.user, key=f'user{id}').strip()
    stream.passwd = st.text_input('Password', stream.passwd, type="password", key=f'passwd{id}').strip()
    stream.url = st.text_input('URL Override', stream.url, key=f'url{id}').strip()
    st.text('URL')
    st.code(stream.get_url_masked(), "markdown")


def setup_channel(channel: Channel, id: str):
    channel.name = st.text_input('Name', channel.name).strip()
    tab_preview, tab_detail = st.tabs(['Preview', 'Detail'])

    with tab_preview:
        setup_stream(channel.preview, f'preview{id}')

    with tab_detail:
        setup_stream(channel.detail, f'detail{id}')


def make_grid(rows: int, cols: int) -> List[List[DeltaGenerator]]:
    grid = []
    for _ in range(rows):
        with st.container():
            columns = st.columns(cols)
            grid.append(columns)
    return grid


def generate_camplayer_ini(config: Config, ini: ConfigParser=ConfigParser(), masked=False) -> str:
    ini['DEVICE1'] = {}
    ini['SCREEN1'] = {'layout': str(config.count)}

    def add_channel(section: SectionProxy, ch: Channel, index: int):
        section[f'channel{index}_name'] = ch.name
        section[f'channel{index}.1_url'] = ch.detail.get_url() if not masked else ch.detail.get_url_masked()
        section[f'channel{index}.2_url'] = ch.preview.get_url() if not masked else ch.preview.get_url_masked()

    for i, ch in enumerate(config.channels):
        add_channel(ini['DEVICE1'], ch, i+1)

    for i, ch_name in enumerate(config.layout):
        try:
            index = config.get_channel_names().index(ch_name)
            ini['SCREEN1'][f'window{i+1}'] = f'device1,channel{index+1}'
        except ValueError:
            st.error(f'Stray channel name in layout: "{ch_name}" (skipped)')

    s = io.StringIO()

    ini.write(s)
    s.seek(0)

    return s.read()


def restart_camplayer() -> bool:
    container = st.empty()

    with st.spinner('Restarting camplayer service ...'):
        start_cmd = 'service camplayer stop && service camplayer start && service camplayer status'
        container.code(start_cmd)

        result = subprocess.run(start_cmd, shell=True, capture_output=True)
        container.code(result.stdout.decode() + '\n\n' + result.stderr.decode())

        #result = subprocess.run('service camplayer start'.split(' '), capture_output=True)
        return result.returncode == 0
