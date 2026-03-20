import streamlit as st

# Initialize board
if "board" not in st.session_state:
    st.session_state.board = [" "]*9
    st.session_state.game_over = False


board = st.session_state.board


# Print board function
def check_winner(player):

    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] == player:
            return True
    return False


def is_draw():
    return " " not in board


# Minimax Algorithm
def minimax(is_max):

    if check_winner("X"):
        return 1
    if check_winner("O"):
        return -1
    if is_draw():
        return 0

    if is_max:

        best = -100

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(False)
                board[i] = " "
                best = max(best, score)

        return best

    else:

        best = 100

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(True)
                board[i] = " "
                best = min(best, score)

        return best


# AI best move
def best_move():

    best_score = -100
    move = None

    for i in range(9):

        if board[i] == " ":

            board[i] = "X"
            score = minimax(False)
            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        board[move] = "X"


# UI Title
st.title("Tic Tac Toe AI (Minimax)")

# Draw board
cols = st.columns(3)

for i in range(9):

    col = cols[i % 3]

    if col.button(board[i] if board[i] != " " else " ", key=i):

        if board[i] == " " and not st.session_state.game_over:

            board[i] = "O"

            if check_winner("O"):
                st.session_state.game_over = True
                st.success("You Win!")
            elif is_draw():
                st.session_state.game_over = True
                st.info("Draw!")
            else:

                best_move()

                if check_winner("X"):
                    st.session_state.game_over = True
                    st.error("AI Wins!")
                elif is_draw():
                    st.session_state.game_over = True
                    st.info("Draw!")

    cols[i % 3] = col


# Reset button
if st.button("Restart Game"):
    st.session_state.board = [" "]*9
    st.session_state.game_over = False
    st.rerun()