import streamlit as st
import random
import copy
from enum import Enum

EMPTY_CELL_CHARACTER = "➖"
PLAYER_1 = "❎" # human
PLAYER_2 = "🅾️" # computer
maximal_score = 1000
minimal_score = -1000

class Intelligence_Level(Enum):
    Dumb = 1
    Smart = 2

def init():
    # Streamlit session state initialization
    st.session_state.matrix_dimension = 3 if 'matrix_dimension' not in st.session_state else st.session_state.matrix_dimension
    st.session_state.board = [[EMPTY_CELL_CHARACTER for _ in range(st.session_state.matrix_dimension)] for _ in range(st.session_state.matrix_dimension)]
    st.session_state.player = PLAYER_1
    st.session_state.opponent = 'Computer'
    st.session_state.winner = None
    st.session_state.row_sum, st.session_state.col_sum = [0] * st.session_state.matrix_dimension, [0] * st.session_state.matrix_dimension
    st.session_state.diag_sum = st.session_state.anti_diag_sum = 0
    st.session_state.move_count = 0
    st.session_state.computer_intelligence = 'Dumb'
    
    
def get_move():
    while True:
        coordinate = random.randint(0, (st.session_state.matrix_dimension**2) - 1)
        row, column = divmod(coordinate, st.session_state.matrix_dimension)
        value_at_coordinate = st.session_state.board[row][column]
        if value_at_coordinate == EMPTY_CELL_CHARACTER:
            return (row, column)

def has_current_player_won(player, move, board_copy):
    row, column = move
    offset = 1 if player == PLAYER_1 else -1

    if not board_copy:
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
    else:
        row_sum_copy = [0] * st.session_state.matrix_dimension
        col_sum_copy = [0] * st.session_state.matrix_dimension
        diag_sum_copy = 0
        anti_diag_sum_copy = 0

        for r in range(len(board_copy)):
            for c in range(len(board_copy)):
                if board_copy[r][c] == EMPTY_CELL_CHARACTER:
                    continue
                elif board_copy[r][c] == player:
                    row_sum_copy[r] += offset
                    col_sum_copy[c] += offset
                    if r == c:
                        diag_sum_copy += offset
                    if r + c == st.session_state.matrix_dimension - 1:
                        anti_diag_sum_copy += offset
                else:
                    row_sum_copy[r] -= offset
                    col_sum_copy[c] -= offset
                    if r == c:
                        diag_sum_copy -= offset
                    if r + c == st.session_state.matrix_dimension - 1:
                        anti_diag_sum_copy -= offset


        if st.session_state.matrix_dimension in {
            row_sum_copy[row],
            col_sum_copy[column],
            diag_sum_copy,
            anti_diag_sum_copy,
        }:
            return True
        if -st.session_state.matrix_dimension in {
            row_sum_copy[row],
            col_sum_copy[column],
            diag_sum_copy,
            anti_diag_sum_copy,
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
        st.session_state.move_count += 1
        if has_current_player_won(st.session_state.player, move, None):
            st.session_state.winner = st.session_state.player
        else:
            st.session_state.player = PLAYER_1 if st.session_state.player == PLAYER_2 else PLAYER_2

def computer_move():
    if are_moves_remaining() and st.session_state.player != PLAYER_1:
        if st.session_state.computer_intelligence == 'Dumb': # dumb computer
            move = get_move()
        else: # smart computer
            move = get_best_move(PLAYER_2, st.session_state.move_count)
        row, column = move
        board_button_click_handler(row, column)
    
def get_best_move(player, move_count):
    best_score = minimal_score if player == PLAYER_2 else maximal_score
    best_move = None

    board_copy = copy.deepcopy(st.session_state.board)
    
    for row in range(len(board_copy)):
        for column in range(len(board_copy)):
            
            if board_copy[row][column] == EMPTY_CELL_CHARACTER:
                # make a move
                move = row, column
                board_copy[row][column] = player
                
                # get score for this move
                score = minimax_alpha_beta(player, move, 0, move_count + 1, minimal_score, maximal_score, board_copy)

                # undo move
                board_copy[row][column] = EMPTY_CELL_CHARACTER

                # recalculate best_score and best_move
                if is_score_better(score, best_score, player):
                    best_score = score
                    best_move = move

    return best_move


def minimax_alpha_beta(player, move, depth, move_count, alpha, beta, board_copy):
    score = get_score(player, move, depth, board_copy)

    # return score - base condition
    if player == PLAYER_2 and score > 0:
        return score # computer won 
    elif player == PLAYER_1 and score < 0:
        return score # human won
    elif move_count == len(board_copy) ** 2: 
        return 0 # last move resulting in a tie
    
    # recursive condition - no one won, find next best move
    
    # switch player for next move
    next_player = PLAYER_1 if player == PLAYER_2 else PLAYER_2
    best_score = minimal_score if next_player == PLAYER_2 else maximal_score
    
    for row in range(len(board_copy)):
        for column in range(len(board_copy)):
            if board_copy[row][column] == EMPTY_CELL_CHARACTER:
                # make a move
                next_move = row, column
                board_copy[row][column] = next_player
                
                # get score for this move
                score = minimax_alpha_beta(next_player, next_move, depth + 1, move_count + 1, alpha, beta, board_copy)

                # undo move
                board_copy[row][column] = EMPTY_CELL_CHARACTER

                if is_score_better(score, best_score, next_player):
                    best_score = score
                    alpha = max(alpha, best_score) if next_player == PLAYER_2 else alpha
                    beta = min(beta, best_score) if next_player == PLAYER_1 else beta
                    if beta <= alpha:
                        break

    return best_score

def is_score_better(score, best_score, player):
        if player == PLAYER_2:
            return score > best_score
        else:
            return score < best_score
        
def get_score(current_player, move, depth, board_copy):
    if has_current_player_won(current_player, move, board_copy):
        
        if current_player == PLAYER_2:
            return maximal_score - depth # computer won 
        else:
            return minimal_score + depth # human won
    else:
        return 0

def streamlit_display():
    header_columns = st.columns([1, 3, 1])
    header_columns[1].title("❎🅾️ Tic Tac Toe")
    st.header("")

    new_game, opponent, difficulty = st.columns([1, 1, 1])
    st.header("")
    
    new_game.button(
        "New game", key="new_game", help="Start a new game", on_click=init
    )

    opponent.radio(
    "Choose your opponent:",
    ('Human', 'Computer'),
    key = 'opponent')

    difficulty.radio(
    "Choose difficulty:",
    ('Dumb', 'Smart'),
    key = 'computer_intelligence')

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
