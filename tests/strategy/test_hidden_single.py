from unittest.mock import Mock

from strategy.hidden_single import HiddenSingleStrategy


def test_finds_hidden_single():
    # ARRANGE
    analysis = Mock()

    cells = [
        Mock(row=3, col=0),
        Mock(row=3, col=1),
        Mock(row=3, col=2),
    ]

    analysis.iterate.units.return_value = (cells,)

    analysis.get_cells_with_candidate.side_effect = [
        (cells[0], cells[1]),  # 1 can go in two cells
        (cells[0], cells[1]),  # 2 can go in two cells
        (cells[1],),  # 3 can only go in cells[1]
    ]

    # ACT
    deduction = HiddenSingleStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Hidden Single"
    assert deduction.cell is cells[1]
    assert deduction.digit == 3
    assert deduction.explanation == ("3 is a hidden single in cell R4C2")


def test_returns_none_when_no_hidden_single():
    # ARRANGE
    analysis = Mock()

    cells = (
        Mock(row=0, col=0),
        Mock(row=0, col=1),
    )

    analysis.iterate.units.return_value = (cells,)

    analysis.get_cells_with_candidate.side_effect = [
        (cells[0], cells[1]),
    ] * 9

    # ACT
    result = HiddenSingleStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_returns_first_hidden_single():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0)
    second = Mock(row=0, col=1)

    cells = [first, second]

    analysis.iterate.units.return_value = (cells,)

    analysis.get_cells_with_candidate.side_effect = [
        (first,),  # 1 is a hidden single
        (second,),  # 2 is also a hidden single
    ]

    # ACT
    deduction = HiddenSingleStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.cell is first
    assert deduction.digit == 1


def test_stops_after_finding_hidden_single():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0)
    second = Mock(row=0, col=1)
    third = Mock(row=0, col=2)

    cells = [first, second, third]

    analysis.iterate.units.return_value = (cells,)

    analysis.get_cells_with_candidate.side_effect = [
        (first,),  # 1 is a hidden single
        (second,),  # 2 should not be checked
        (third,),  # 3 should not be checked
    ]

    # ACT
    HiddenSingleStrategy().find(analysis)

    # ASSERT
    assert analysis.get_cells_with_candidate.call_count == 1
