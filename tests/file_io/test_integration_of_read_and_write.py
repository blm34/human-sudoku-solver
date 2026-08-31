from io import StringIO

from persistance.readers.susser import SusserReader
from persistance.writers.susser import SusserWriter
from grid import GridState


def test_susser_round_trip():
    # ARRANGE
    original = GridState()
    original.values = list(range(1, 10)) * 9

    stream = StringIO()

    # ACT
    SusserWriter().write(original, stream)

    stream.seek(0)

    result = SusserReader().read(stream)

    # ASSERT
    assert result.values == original.values
