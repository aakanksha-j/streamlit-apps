import streamlit as st
import random

class TicTacToe:
    def __init__(self):
        self.n = 3
        self.board = [['.' for _ in range(self.n)] for _ in range(self.n)]
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.row_sum, self.col_sum = [0] * self.n, [0] * self.n
        self.diag_sum = self.anti_diag_sum = 0

    def make_move(self, player):
        while True:
            coordinate = random.randint(0, (self.n ** 2) -1)
            row, column = divmod(coordinate, self.n)
            value_at_coordinate = self.board[row][column]
            if value_at_coordinate == '.':
                self.board[row][column] = player
                return (row, column)    

    def print_board(self):
        for i in range(self.n):
            st.write(self.board[i])
        st.write()

    def has_current_player_won(self, player, move):
        row, column = move
        offset = 1 if player == 'x' else -1

        self.row_sum[row] += offset
        self.col_sum[column] += offset

        if row == column:
            self.diag_sum += offset
        if row + column == self.n - 1:
            self.anti_diag_sum += offset

        if self.n in {self.row_sum[row], self.col_sum[column], self.diag_sum, self.anti_diag_sum}:
            return True
        if -self.n in {self.row_sum[row], self.col_sum[column], self.diag_sum, self.anti_diag_sum}:
            return True
        return False

    def run_game(self): 
        self.print_board()
        for i in range(self.n ** 2):
            player = self.player_1 if i%2 != 0 else self.player_2
            move = self.make_move(player)
            self.print_board()
            if self.has_current_player_won(player, move):
                st.write(player, 'has won!')
                return
        st.write('It is a tie!')
            


def main():
    # st.write(
    #     """
    #     # ❎🅾️ Tic Tac Toe
    #     """
    # )
    st.write("❎🅾️ Tic Tac Toe")
    tictactoe = TicTacToe()
    tictactoe.run_game()
    
    
if __name__ == '__main__':
    main()