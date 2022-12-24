import streamlit as st
import random

EMPTY_CELL_CHARACTER = "➖"
PLAYER_1 = "❎" # human
PLAYER_2 = "🅾️" # computer

def init():
    # Streamlit session state initialization
    st.session_state.matrix_dimension = 3 if 'matrix_dimension' not in st.session_state else st.session_state.matrix_dimension
    st.session_state.board = [[EMPTY_CELL_CHARACTER for _ in range(st.session_state.matrix_dimension)] for _ in range(st.session_state.matrix_dimension)]
    st.session_state.player = PLAYER_1
    st.session_state.opponent = 'Computer'
    st.session_state.winner = None
    st.session_state.row_sum, st.session_state.col_sum = [0] * st.session_state.matrix_dimension, [0] * st.session_state.matrix_dimension
    st.session_state.diag_sum = st.session_state.anti_diag_sum = 0
    
def get_move():
    while True:
        coordinate = random.randint(0, (st.session_state.matrix_dimension**2) - 1)
        row, column = divmod(coordinate, st.session_state.matrix_dimension)
        value_at_coordinate = st.session_state.board[row][column]
        if value_at_coordinate == EMPTY_CELL_CHARACTER:
            return (row, column)

def has_current_player_won(player, move):
    row, column = move
    offset = 1 if player == PLAYER_1 else -1

    st.session_state.row_sum[row] += offset
    st.session_state.col_sum[column] += offset

    if row == column:
        st.session_state.diag_sum += offset
    if row + column == st.session_state.matrix_dimension - 1:
        st.session_state.anti_diag_sum += offset

    if st.session_state.matrix_dimension in {
        st.session_state.row_sum[row],
        st.session_state.col_sum[column],
        st.session_state.diag_sum,
        st.session_state.anti_diag_sum,
    }:
        return True
    if -st.session_state.matrix_dimension in {
        st.session_state.row_sum[row],
        st.session_state.col_sum[column],
        st.session_state.diag_sum,
        st.session_state.anti_diag_sum,
    }:
        return True
    return False

def are_moves_remaining():
    for i in range(st.session_state.matrix_dimension):
        for j in range(st.session_state.matrix_dimension):
            if st.session_state.board[i][j] == EMPTY_CELL_CHARACTER:
                return True
    return False

def evaluate_game_state():
    if st.session_state.winner:
        st.success(f"{st.session_state.winner} won the game! 🎉")
    elif not are_moves_remaining() and not st.session_state.winner:
        st.info(f'It is a tie! 🥈')

def board_button_click_handler(i, j):
    if not st.session_state.winner and st.session_state.board[i][j] != EMPTY_CELL_CHARACTER:
        st.warning("⚠️ This move has been made already")
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i][j] = st.session_state.player
        move = i, j
        if has_current_player_won(st.session_state.player, move):
            st.session_state.winner = st.session_state.player
        else:
            st.session_state.player = PLAYER_1 if st.session_state.player == PLAYER_2 else PLAYER_2

def computer_move():
    if are_moves_remaining() and st.session_state.player == PLAYER_2:
        move = get_move()
        row, column = move
        board_button_click_handler(row, column)

def streamlit_display():
    st.header("❎🅾️ Tic Tac Toe")

    new_game, opponent, size = st.columns([1, 1, 1])
    
    new_game.button(
        "New game", key="new_game", help="Start a new game", on_click=init
    )

    opponent.radio(
    "Choose your opponent:",
    ('Human', 'Computer'),
    key = 'opponent')

    size.slider('Choose game board size (game restarts):', 2, 10, key = 'matrix_dimension', on_change=init)

    # Tic Tac Toe Board
    for i, row in enumerate(st.session_state.board):
        column_array = [2] + [1] * st.session_state.matrix_dimension + [2]
        columns = st.columns(column_array)
        for j, value in enumerate(row):
            columns[j + 1].button(
                value,
                key=f"{i}-{j}",
                on_click=board_button_click_handler,
                args=(i, j),
            )

def main():
    if "board" not in st.session_state:
        init()
    
    if st.session_state.opponent == 'Computer':
        computer_move()

    streamlit_display()

    evaluate_game_state()

if __name__ == "__main__":
    main()
