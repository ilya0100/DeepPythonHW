class TicTacGame:

    def __init__(self):
        self.board = []

        for _ in range(3):
            self.board.append([' '] * 3)

        self.turn = 0

    def show_board(self):
        for i in range(3):
            print(self.board[i][0], self.board[i][1],
                  self.board[i][2], sep='|')
            if i != 2:
                print('-' * 5)

    def show_whose_turn(self):
        if self.turn % 2 == 0:
            print("X turn")
        else:
            print("O turn")

    def validate_input(self, coordinates):
        if 0 <= coordinates[0] <= 2 and 0 <= coordinates[1] <= 2:
            return self.board[coordinates[0]][coordinates[1]] == ' '

        print("Coordinates must be in the range 0..2")
        return False

    def make_turn(self, coordinates):
        if self.turn % 2 == 0:
            self.board[coordinates[0]][coordinates[1]] = 'X'
        else:
            self.board[coordinates[0]][coordinates[1]] = 'O'

    def start_game(self):
        while (not self.check_winner() and self.turn < 9):
            self.show_whose_turn()

            coordinates = self.get_coordinates()
            if coordinates is None:
                continue

            if self.validate_input(coordinates):
                self.make_turn(coordinates)
                self.turn += 1

            self.show_board()
            print()

        if self.turn == 9:
            return "No one"
        if self.turn % 2 == 0:
            return 'O'
        return 'X'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True

            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

    def get_coordinates(self):
        try:
            coordinates = tuple(map(int, input().split()))
            if len(coordinates) != 2:
                raise ValueError

        except ValueError:
            print("Input is incorrect. Use: 'row' 'column'")
            print("Example: 0 1")
            return None

        return coordinates


if __name__ == "__main__":
    game = TicTacGame()
    print(game.start_game(), "wins!")
