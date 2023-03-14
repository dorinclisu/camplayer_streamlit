"""
Behaves exactly like python -m streamlit [args], except it mocks the pyarrow dependency
"""

import mock_pyarrow
from streamlit.web.cli import main



main(prog_name='streamlit')
