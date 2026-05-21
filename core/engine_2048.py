import random


class Engine2048:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            # 10% chance to spawn a 4, 90% chance to spawn a 2
            self.board[r][c] = 4 if random.random() < 0.1 else 2

    def _compress(self, row):
        # Remove zeros and slide numbers to the left
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def _merge(self, row):
        # Merge identical adjacent numbers
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def _slide_left(self):
        changed = False
        for i in range(4):
            original = list(self.board[i])
            # To move left: compress -> merge -> compress again
            compressed = self._compress(self.board[i])
            merged = self._merge(compressed)
            self.board[i] = self._compress(merged)
            if original != self.board[i]:
                changed = True
        return changed

    def _transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def _reverse_rows(self):
        for i in range(4):
            self.board[i].reverse()

    def move(self, direction):
        if self.game_over:
            return False

        changed = False
        if direction == "LEFT":
            changed = self._slide_left()
        elif direction == "RIGHT":
            self._reverse_rows()
            changed = self._slide_left()
            self._reverse_rows()
        elif direction == "UP":
            self._transpose()
            changed = self._slide_left()
            self._transpose()
        elif direction == "DOWN":
            self._transpose()
            self._reverse_rows()
            changed = self._slide_left()
            self._reverse_rows()
            self._transpose()

        if changed:
            self.spawn_tile()
            self.check_game_over()

        return changed

    def check_game_over(self):
        # If there's an empty space, game is not over
        for r in range(4):
            for c in range(4):
                if self.board[r][c] == 0:
                    return

        # If there are adjacent matching numbers, game is not over
        for r in range(4):
            for c in range(3):
                if self.board[r][c] == self.board[r][c + 1]:
                    return
        for r in range(3):
            for c in range(4):
                if self.board[r][c] == self.board[r + 1][c]:
                    return

        self.game_over = True