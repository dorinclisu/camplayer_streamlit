import time

import numpy as np
import pandas as pd
import streamlit as st

from common import *



config = load()

config.count = st.selectbox('Window Count', get_args(WindowCount), get_args(WindowCount).index(config.count))  # type: ignore[assignment]

for name in config.layout.copy():
    if name not in config.get_channel_names():
        st.error(f'Stray channel name in layout: "{name}" (removed)')
        config.layout.remove(name)

config.layout = st.multiselect('Window Layout', config.get_channel_names(), config.layout)

if len(config.layout) > config.count:
    st.error(f'Layout must have maximum {config.count} windows!')
else:
    with st.container():
        n = int(np.ceil(np.sqrt(config.count)))

        df = pd.DataFrame([['' for col in range(n)] for row in range(n)], dtype=str)

        for i, name in enumerate(config.layout):
            row = i // n
            col = i % n
            df[col][row] = name

        # style = df.style
        # style = style.hide(axis='columns').hide(axis='rows')
        # st.write(style.to_html(), unsafe_allow_html=True)
        # st.text('')
        hide_table_row_index = """
            <style>
            thead tr {display:none}
            tbody th {display:none}
            </style>
            """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df)

    if st.button('Save'):
        save(config)
        st.markdown(':green[Saved]')
        time.sleep(1)
        st.experimental_rerun()  # we need this to avoid weird behavior with widgets not working right after save
