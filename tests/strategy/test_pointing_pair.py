from unittest.mock import Mock

from sudoku_strategy.strategy.pointing_pair import PointingPair, PointingPairStrategy


def test_finds_pointing_pair_in_row():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=0)
    second = Mock(row=0, col=1, box=0)
    third = Mock(row=0, col=2, box=0)
    fourth = Mock(row=0, col=3, box=1)

    box_cells = (first, second, third)
    row_cells = (first, second, third, fourth)

    analysis.iterate.box.return_value = box_cells
    analysis.get_cells_with_candidate.return_value = box_cells
    analysis.iterate.row.return_value = row_cells

    analysis.cell_has_candidate.return_value = True

    # ACT
    deduction = PointingPairStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Pointing Pair"
    assert deduction.eliminations == [(fourth, 1)]
    assert deduction.explanation == (
        "Candidates for 1 in box 0 allow for eliminations in R1C4."
    )


def test_finds_pointing_pair_in_column():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=0)
    second = Mock(row=1, col=0, box=0)
    third = Mock(row=3, col=0, box=4)

    box_cells = (first, second, Mock(row=1, col=1, box=0))
    col_cells = (first, second, third)

    analysis.iterate.box.return_value = box_cells
    analysis.get_cells_with_candidate.return_value = (first, second)
    analysis.iterate.col.return_value = col_cells

    analysis.cell_has_candidate.return_value = True

    # ACT
    deduction = PointingPairStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Pointing Pair"
    assert deduction.eliminations == [(third, 1)]
    assert deduction.explanation == (
        "Candidates for 1 in box 0 allow for eliminations in R4C1."
    )


def test_returns_none_when_no_pointing_pair():
    # ARRANGE
    analysis = Mock()

    cells = (
        Mock(row=0, col=0, box=0),
        Mock(row=0, col=1, box=0),
        Mock(row=1, col=0, box=0),
    )

    analysis.iterate.box.return_value = cells
    analysis.get_cells_with_candidate.return_value = cells

    # ACT
    result = PointingPairStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_returns_none_when_pointing_pair_has_no_eliminations():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=0)
    second = Mock(row=0, col=1, box=0)
    third = Mock(row=0, col=2, box=0)
    fourth = Mock(row=0, col=3, box=1)

    analysis.iterate.box.return_value = (first, second)
    analysis.get_cells_with_candidate.return_value = (first, second)
    analysis.cell_has_candidate.return_value = False
    analysis.iterate.row.return_value = (first, second, third, fourth)

    # ACT
    result = PointingPairStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_skips_candidate_when_more_than_three_cells_have_it():
    # ARRANGE
    analysis = Mock()

    cells = (
        Mock(row=0, col=0),
        Mock(row=0, col=1),
        Mock(row=0, col=2),
        Mock(row=1, col=0),
    )

    analysis.iterate.box.return_value = cells
    analysis.get_cells_with_candidate.return_value = cells

    # ACT
    result = PointingPairStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_skips_digit_when_no_cells_have_candidate():
    # ARRANGE
    analysis = Mock()

    box_cells = (
        Mock(row=0, col=0),
        Mock(row=0, col=1),
    )

    analysis.iterate.box.return_value = box_cells
    analysis.get_cells_with_candidate.return_value = ()

    # ACT
    result = PointingPairStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_finds_first_pointing_pair_with_elimination():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=0)
    second = Mock(row=0, col=1, box=0)
    first_elimination = Mock(row=0, col=3, box=1)
    second_elimination = Mock(row=0, col=4, box=1)

    analysis.iterate.box.return_value = (first, second)

    analysis.get_cells_with_candidate.side_effect = [
        (),
        (first, second),
    ]

    analysis.iterate.row.return_value = (
        first,
        second,
        first_elimination,
        second_elimination,
    )

    analysis.cell_has_candidate.side_effect = [True, False]

    # ACT
    deduction = PointingPairStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Pointing Pair"
    assert deduction.eliminations == [(first_elimination, 2)]


def test_get_eliminations_ignores_cells_in_pointing_pair_box():
    # ARRANGE
    analysis = Mock()

    box_cell = Mock(row=0, col=0, box=0)
    elimination_cell = Mock(row=0, col=3, box=1)

    pointing_pair = PointingPair(
        digit=5,
        box=0,
        cells=(box_cell, elimination_cell),
    )

    analysis.cell_has_candidate.return_value = True

    # ACT
    eliminations = PointingPairStrategy()._get_eliminations(
        analysis,
        pointing_pair,
    )

    # ASSERT
    assert eliminations == [(elimination_cell, 5)]
    analysis.cell_has_candidate.assert_called_once_with(
        elimination_cell,
        5,
    )


def test_get_eliminations_only_returns_cells_with_candidate():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=1)
    second = Mock(row=0, col=1, box=2)
    third = Mock(row=0, col=2, box=3)

    pointing_pair = PointingPair(
        digit=7,
        box=0,
        cells=(first, second, third),
    )

    analysis.cell_has_candidate.side_effect = [True, False, True]

    # ACT
    eliminations = PointingPairStrategy()._get_eliminations(
        analysis,
        pointing_pair,
    )

    # ASSERT
    assert eliminations == [
        (first, 7),
        (third, 7),
    ]


def test_get_eliminations_returns_empty_when_no_cells_have_candidate():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0, box=1)
    second = Mock(row=0, col=1, box=2)

    pointing_pair = PointingPair(
        digit=3,
        box=0,
        cells=(first, second),
    )

    analysis.cell_has_candidate.return_value = False

    # ACT
    eliminations = PointingPairStrategy()._get_eliminations(
        analysis,
        pointing_pair,
    )

    # ASSERT
    assert eliminations == []
