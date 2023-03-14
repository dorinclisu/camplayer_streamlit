import logging
import sys
from unittest.mock import MagicMock


pyarrow = MagicMock()
pyarrow.__version__ = '11.0.0'

class MockTable:
    def __new__(cls, *args, **kwargs):
        return MagicMock(spec=cls)

pyarrow.Table = MockTable

pyarrow_compute = MagicMock()

sys.modules['pyarrow'] = pyarrow
sys.modules['pyarrow.compute'] = pyarrow_compute

logging.warning('Running without pyarrow functionality (mocked)! Make sure that dataframe serialization is set to legacy mode.')
