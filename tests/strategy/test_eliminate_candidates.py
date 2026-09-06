from unittest.mock import Mock

from sudoku_strategy.strategy.eliminate_candidates import EliminateCandidatesStrategy


def test_finds_eliminatable_candidate():
    # ARRANGE
    analysis = Mock()

    filled_cell = Mock(row=0, col=0)
    peer = Mock(row=0, col=1)

    analysis.iterate.filled_cells.return_value = [filled_cell]
    analysis.get_value_in_cell.return_value = 5
    analysis.iterate.peers.return_value = [peer]
    analysis.get_cells_with_candidate.return_value = [peer]

    # ACT
    deduction = EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.strategy == "Candidate Elimination"
    assert deduction.eliminations == [(peer, 5)]
    assert deduction.explanation == (
        "The given candidates are already accounted for in a given unit"
    )


def test_returns_none_when_no_candidates_can_be_eliminated():
    # ARRANGE
    analysis = Mock()

    filled_cell = Mock(row=0, col=0)
    peer = Mock(row=0, col=1)

    analysis.iterate.filled_cells.return_value = [filled_cell]
    analysis.get_value_in_cell.return_value = 5
    analysis.iterate.peers.return_value = [peer]
    analysis.get_cells_with_candidate.return_value = []

    # ACT
    result = EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    assert result is None


def test_finds_multiple_eliminatable_candidates():
    # ARRANGE
    analysis = Mock()

    filled_cell = Mock(row=0, col=0)
    first_peer = Mock(row=0, col=1)
    second_peer = Mock(row=1, col=0)

    analysis.iterate.filled_cells.return_value = [filled_cell]
    analysis.get_value_in_cell.return_value = 5
    analysis.iterate.peers.return_value = [first_peer, second_peer]
    analysis.get_cells_with_candidate.return_value = [
        first_peer,
        second_peer,
    ]

    # ACT
    deduction = EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.eliminations == [
        (first_peer, 5),
        (second_peer, 5),
    ]


def test_finds_eliminations_from_multiple_filled_cells():
    # ARRANGE
    analysis = Mock()

    first_filled = Mock(row=0, col=0)
    second_filled = Mock(row=1, col=1)

    first_peer = Mock(row=0, col=1)
    second_peer = Mock(row=1, col=2)

    analysis.iterate.filled_cells.return_value = (
        first_filled,
        second_filled,
    )

    analysis.get_value_in_cell.side_effect = [5, 7]

    analysis.iterate.peers.side_effect = [
        [first_peer],
        [second_peer],
    ]

    analysis.get_cells_with_candidate.side_effect = [
        [first_peer],
        [second_peer],
    ]

    # ACT
    deduction = EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    assert deduction is not None
    assert deduction.eliminations == [
        (first_peer, 5),
        (second_peer, 7),
    ]


def test_checks_all_filled_cells():
    # ARRANGE
    analysis = Mock()

    first = Mock(row=0, col=0)
    second = Mock(row=0, col=1)
    third = Mock(row=0, col=2)

    analysis.iterate.filled_cells.return_value = (first, second, third)

    analysis.get_value_in_cell.side_effect = [5, 6, 7]
    analysis.iterate.peers.side_effect = [
        [],
        [],
        [],
    ]
    analysis.get_cells_with_candidate.return_value = []

    # ACT
    result = EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    assert result is None
    assert analysis.get_value_in_cell.call_count == 3
    assert analysis.iterate.peers.call_count == 3
    assert analysis.get_cells_with_candidate.call_count == 3


def test_gets_candidates_for_filled_cell_value_from_its_peers():
    # ARRANGE
    analysis = Mock()

    filled_cell = Mock(row=3, col=6)
    peers = (
        Mock(row=3, col=0),
        Mock(row=3, col=1),
    )

    analysis.iterate.filled_cells.return_value = [filled_cell]
    analysis.get_value_in_cell.return_value = 5
    analysis.iterate.peers.return_value = peers
    analysis.get_cells_with_candidate.return_value = []

    # ACT
    EliminateCandidatesStrategy().find(analysis)

    # ASSERT
    analysis.get_value_in_cell.assert_called_once_with(filled_cell)
    analysis.iterate.peers.assert_called_once_with(filled_cell)
    analysis.get_cells_with_candidate.assert_called_once_with(peers, 5)
