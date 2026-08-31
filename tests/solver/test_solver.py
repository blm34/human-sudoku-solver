from unittest.mock import Mock, call, patch

from solver.solver import Solver


class TestSolver:
    def test_find_next_returns_deduction_from_first_strategy(self):
        # ARRANGE
        grid = Mock()
        analysis = Mock()

        first_strategy = Mock()
        second_strategy = Mock()

        deduction = Mock()

        first_strategy.find.return_value = deduction

        with patch("solver.solver.GridAnalysis", return_value=analysis):
            solver = Solver(strategies=(first_strategy, second_strategy))

            # ACT
            result = solver.find_next(grid)

            # ASSERT
            assert result is deduction
            first_strategy.find.assert_called_once_with(analysis)
            second_strategy.find.assert_not_called()

    def test_find_next_tries_next_strategy_when_first_finds_nothing(self):
        # ARRANGE
        grid = Mock()
        analysis = Mock()

        first_strategy = Mock()
        second_strategy = Mock()

        deduction = Mock()

        first_strategy.find.return_value = None
        second_strategy.find.return_value = deduction

        with patch("solver.solver.GridAnalysis", return_value=analysis):
            solver = Solver(strategies=(first_strategy, second_strategy))

            # ACT
            result = solver.find_next(grid)

            # ASSERT
            assert result is deduction

            first_strategy.find.assert_called_once_with(analysis)
            second_strategy.find.assert_called_once_with(analysis)

    def test_find_next_returns_none_when_no_strategy_finds_deduction(self):
        # ARRANGE
        grid = Mock()
        analysis = Mock()

        first_strategy = Mock()
        second_strategy = Mock()

        first_strategy.find.return_value = None
        second_strategy.find.return_value = None

        with patch("solver.solver.GridAnalysis", return_value=analysis):
            solver = Solver(strategies=(first_strategy, second_strategy))

            # ACT
            result = solver.find_next(grid)

            # ASSERT
            assert result is None

            first_strategy.find.assert_called_once_with(analysis)
            second_strategy.find.assert_called_once_with(analysis)

    def test_find_next_creates_analysis_for_grid(self):
        # ARRANGE
        grid = Mock()
        analysis = Mock()
        strategy = Mock()

        strategy.find.return_value = Mock()

        with patch(
            "solver.solver.GridAnalysis",
            return_value=analysis,
        ) as analysis_class:
            solver = Solver(strategies=(strategy,))

            # ACT
            solver.find_next(grid)

            # ASSERT
            analysis_class.assert_called_once_with(grid)

    def test_solve_uses_copy_of_grid(self):
        # ARRANGE
        grid = Mock()
        working_grid = Mock()

        grid.copy.return_value = working_grid
        working_grid.is_complete.side_effect = [True]

        with patch("solver.solver.GridModifier") as modifier_class:
            solver = Solver()

            # ACT
            result = solver.solve(grid)

            # ASSERT
            grid.copy.assert_called_once()
            modifier_class.assert_called_once_with(working_grid)
            assert result == []

    def test_solve_finds_and_applies_deductions(self):
        # ARRANGE
        grid = Mock()
        working_grid = Mock()

        grid.copy.return_value = working_grid

        deduction = Mock()

        working_grid.is_complete.side_effect = [False, True]

        with (
            patch.object(
                Solver,
                "find_next",
                side_effect=[deduction],
            ),
            patch("solver.solver.GridModifier") as modifier_class,
        ):
            modifier = modifier_class.return_value

            solver = Solver()

            # ACT
            result = solver.solve(grid)

            # ASSERT
            assert result == [deduction]

            grid.copy.assert_called_once()
            modifier_class.assert_called_once_with(working_grid)
            modifier.apply.assert_called_once_with(deduction)

    def test_solve_finds_and_applies_multiple_deductions(self):
        # ARRANGE
        grid = Mock()
        working_grid = Mock()

        grid.copy.return_value = working_grid

        first_deduction = Mock()
        second_deduction = Mock()

        working_grid.is_complete.side_effect = [False, False, True]

        with (
            patch.object(
                Solver,
                "find_next",
                side_effect=[first_deduction, second_deduction],
            ),
            patch("solver.solver.GridModifier") as modifier_class,
        ):
            modifier = modifier_class.return_value

            solver = Solver()

            # ACT
            result = solver.solve(grid)

            # ASSERT
            assert result == [
                first_deduction,
                second_deduction,
            ]

            assert modifier.apply.call_args_list == [
                call(first_deduction),
                call(second_deduction),
            ]

    def test_solve_stops_when_no_deduction_is_found(self):
        # ARRANGE
        grid = Mock()
        working_grid = Mock()

        grid.copy.return_value = working_grid
        working_grid.is_complete.return_value = False

        with (
            patch.object(
                Solver,
                "find_next",
                return_value=None,
            ),
            patch("solver.solver.GridModifier"),
        ):
            solver = Solver()

            # ACT
            result = solver.solve(grid)

            # ASSERT
            assert result == []

    def test_solve_logs_warning_when_no_deduction_is_found(self, caplog):
        # ARRANGE
        grid = Mock()
        working_grid = Mock()

        grid.copy.return_value = working_grid
        working_grid.is_complete.return_value = False

        with (
            patch.object(
                Solver,
                "find_next",
                return_value=None,
            ),
            patch("solver.solver.GridModifier"),
        ):
            solver = Solver()

            # ACT
            solver.solve(grid)

            # ASSERT
            assert "No next step found for puzzle." in caplog.text
