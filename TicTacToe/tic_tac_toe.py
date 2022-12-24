import streamlit as st
import random

MATRIX_DIMENSION = 3
EMPTY_CELL_CHARACTER = "➖"
PLAYER_1 = "❎" # human
PLAYER_2 = "🅾️" # computer

def init():
    # Streamlit session state initialization
    st.session_state.board = [[EMPTY_CELL_CHARACTER for _ in range(MATRIX_DIMENSION)] for _ in range(MATRIX_DIMENSION)]
    st.session_state.player = PLAYER_1
    st.session_state.winner = None
    st.session_state.row_sum, st.session_state.col_sum = [0] * MATRIX_DIMENSION, [0] * MATRIX_DIMENSION
    st.session_state.diag_sum = st.session_state.anti_diag_sum = 0

def get_move():
    while True:
        coordinate = random.randint(0, (MATRIX_DIMENSION**2) - 1)
        row, column = divmod(coordinate, MATRIX_DIMENSION)
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
    if row + column == MATRIX_DIMENSION - 1:
        st.session_state.anti_diag_sum += offset

    if MATRIX_DIMENSION in {
        st.session_state.row_sum[row],
        st.session_state.col_sum[column],
        st.session_state.diag_sum,
        st.session_state.anti_diag_sum,
    }:
        return True
    if -MATRIX_DIMENSION in {
        st.session_state.row_sum[row],
        st.session_state.col_sum[column],
        st.session_state.diag_sum,
        st.session_state.anti_diag_sum,
    }:
        return True
    return False

def are_moves_remaining():
    for i in range(MATRIX_DIMENSION):
        for j in range(MATRIX_DIMENSION):
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

    st.button(
        "New game", key="new_game", help="Start a new game", on_click=init
    )

    # Tic Tac Toe Board
    for i, row in enumerate(st.session_state.board):
        columns = st.columns([5, 1, 1, 1, 5])
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
    
    computer_move()

    streamlit_display()

    evaluate_game_state()

if __name__ == "__main__":
    main()
