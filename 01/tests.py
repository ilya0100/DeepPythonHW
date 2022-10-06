import io
import sys
import unittest
import contextlib

from tic_tac import TicTacGame


class TestTicTac(unittest.TestCase):
    def test_init(self):
        game = TicTacGame()

        for i in range(3):
            for j in range(3):
                self.assertEqual(game.board[i][j], ' ')

        self.assertEqual(game.turn, 0)

    def test_get_coordinates_correct(self):
        game = TicTacGame()

        test_input = io.StringIO("0 0")
        sys.stdin = test_input

        self.assertEqual(game.get_coordinates(), (0, 0))

    def test_get_coordinates_incorrect(self):
        game = TicTacGame()

        test_input = io.StringIO("1 ²")
        sys.stdin = test_input

        test_output = io.StringIO()
        sys.stdout = test_output

        self.failureException(game.get_coordinates())

        test_input = io.StringIO("2")
        sys.stdin = test_input

        self.failureException(game.get_coordinates())

        test_input = io.StringIO("2;")
        sys.stdin = test_input

        self.failureException(game.get_coordinates())

        test_input = io.StringIO("asd")
        sys.stdin = test_input

        self.failureException(game.get_coordinates())

    def test_validate_input_correct(self):
        game = TicTacGame()

        for i in range(3):
            for j in range(3):
                self.assertTrue(game.validate_input((i, j)))

    def test_make_turn(self):
        game = TicTacGame()

        for i in range(3):
            for j in range(3):
                game.make_turn((i, j))

                if game.turn % 2 == 0:
                    self.assertEqual(game.board[i][j], 'X')
                else:
                    self.assertEqual(game.board[i][j], 'O')

                game.turn += 1

    def test_validate_input_incorrect(self):
        game = TicTacGame()

        with contextlib.redirect_stdout(None):
            self.assertFalse(game.validate_input((-1, 0)))
            self.assertFalse(game.validate_input((1, 6)))
            self.assertFalse(game.validate_input((-1, 6)))

        for i in range(3):
            for j in range(3):
                game.make_turn((i, j))

                self.assertFalse(game.validate_input((i, j)))

    def test_check_winner(self):
        for i in range(3):
            game = TicTacGame()
            self.assertFalse(game.check_winner())

            for j in range(3):
                game.make_turn((i, j))

            self.assertTrue(game.check_winner())

        for i in range(3):
            game = TicTacGame()
            self.assertFalse(game.check_winner())

            for j in range(3):
                game.make_turn((j, i))

            self.assertTrue(game.check_winner())

        game = TicTacGame()
        for i in range(3):
            game.make_turn((i, i))

        self.assertTrue(game.check_winner())

        game = TicTacGame()
        for i in range(3):
            game.make_turn((i, 2 - i))

        self.assertTrue(game.check_winner())

    def test_start_game(self):
        game = TicTacGame()

        test_input = io.StringIO("1 1\n2 1\n0 2\n2 1\n2 0\n2 2\n0 0\n1 2\n")
        sys.stdin = test_input

        test_output = io.StringIO()
        sys.stdout = test_output

        self.assertEqual(game.start_game(), "X")

        game = TicTacGame()

        test_input = io.StringIO("1 2\n1 1\n1 0\n2 0\n0 2\n2 2\n2 1\n0 0\n")
        sys.stdin = test_input

        game.start_game()
        self.assertEqual(game.start_game(), "O")

        game = TicTacGame()

        test_input = io.StringIO("0 0\n0 1\n0 2\n1 0\n1 1\n1 2\n2 1\n2 0\n2 2")
        sys.stdin = test_input

        game.start_game()
        self.assertEqual(game.start_game(), "No one")
