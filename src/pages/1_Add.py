

import streamlit as st

from common import *



config = load()

with st.form('add'):
    channel = Channel(
        name='',
        preview=ChannelStream(),
        detail=ChannelStream(hd=True)
    )
    setup_channel(channel, 'add')

    if st.form_submit_button('Add'):
        if not channel.name:
            st.error('Name cannot be blank!')

        elif channel.name in config.get_channel_names():
            st.error(f'Name "{channel.name}" already exists!')
        else:
            config.channels.append(channel)

            if len(config.layout) < config.count and channel.name not in config.layout:
                config.layout.append(channel.name)

            save(config)
            st.markdown(':green[Added]')


with st.sidebar:
    st.markdown('Channels\n' + '\n'.join([f'- {name}' for name in config.get_channel_names()]))
