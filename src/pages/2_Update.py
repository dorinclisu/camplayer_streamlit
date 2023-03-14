import sys
import time

import streamlit as st

from common import *



config = load()

with st.sidebar:
    ch_index = st.radio('Channels', range(len(config.channels)), format_func=lambda i: config.channels[i].name)

if ch_index is None:
    st.text('Add a channel first')
    sys.exit()

channel = config.channels[ch_index]


if st.button('🗑 Delete'):
    st.session_state.delete_attempt = True

if st.session_state.get('delete_attempt'):
    st.warning(f'Are you sure you want to delete "{channel.name}" ?')

    col1, col2 = st.columns(2)

    if col1.button('No'):
        st.session_state.delete_attempt = False
        st.experimental_rerun()

    if col2.button('Yes'):
        st.session_state.delete_attempt = False

        del config.channels[ch_index]

        if channel.name in config.layout:
            config.layout.remove(channel.name)

        save(config)

        st.markdown(':green[Deleted]')
        time.sleep(1)
        st.experimental_rerun()


with st.form('update'):
    setup_channel(channel, 'update')

    if st.form_submit_button('Update'):
        if not channel.name:
            st.error('Name cannot be blank!')
        else:
            # Update channel name in layout
            for i, name in enumerate(config.layout.copy()):
                if name not in config.get_channel_names():  #  this is a hack because we don't have access to previous name of channel
                    config.layout[i] = channel.name

            save(config)

            st.markdown(':green[Updated]')
            time.sleep(1)
            st.experimental_rerun()
