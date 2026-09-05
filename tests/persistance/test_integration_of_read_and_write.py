from io import StringIO

from grid import GridState
from persistance.readers.susser import SusserReader
from persistance.writers.susser import SusserWriter


def test_susser_round_trip():
    # ARRANGE
    original = GridState.create_empty()
    original._values = list(range(1, 10)) * 9

    stream = StringIO()

    # ACT
    SusserWriter().write(original, stream)

    stream.seek(0)

    result = SusserReader().read(stream)

    # ASSERT
    assert result._values == original._values
