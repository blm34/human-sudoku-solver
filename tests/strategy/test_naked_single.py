from unittest.mock import Mock

from strategy.naked_single import NakedSingleStrategy


def test_finds_naked_single():
    # ARRANGE
    analysis = Mock()

    cell = Mock(row=3, col=6)

    analysis.iterate.empty_cells.return_value = [cell]
    analysis.count_candidates_in_cell.return_value = 1
    analysis.get_candidates_for_cell.return_value = tuple([5])

    # ACT
    deduction = NakedSingleStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Naked Single"
    assert deduction.cell is cell
    assert deduction.digit == 5
    assert deduction.explanation == ("Cell R4C7 is a naked single with value 5.")


def test_returns_none_when_no_naked_single():
    # ARRANGE
    analysis = Mock()

    cells = (
        Mock(row=0, col=0),
        Mock(row=0, col=1),
        Mock(row=0, col=2),
    )

    analysis.iterate.empty_cells.return_value = cells
    analysis.count_candidates_in_cell.side_effect = [2, 3, 4]

    # ACT
    result = NakedSingleStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_returns_first_naked_single():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0)
    second = Mock(row=4, col=5)

    analysis.iterate.empty_cells.return_value = (first, second)
    analysis.count_candidates_in_cell.side_effect = [2, 1]
    analysis.get_candidates_for_cell.return_value = (7,)

    # ACT
    deduction = NakedSingleStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.cell is second
    assert deduction.digit == 7


def test_stops_after_finding_naked_single():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0)
    second = Mock(row=0, col=1)
    third = Mock(row=0, col=2)

    analysis.iterate.empty_cells.return_value = (first, second, third)
    analysis.count_candidates_in_cell.side_effect = [2, 1, 1]
    analysis.get_candidates_for_cell.return_value = (4,)

    # ACT
    NakedSingleStrategy().find(analysis)

    # ASSERT
    assert analysis.count_candidates_in_cell.call_count == 2
