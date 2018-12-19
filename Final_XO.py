import random


def draw_board(board):
    """
    print out a board after any player makes a move
    :param board: the clear board
    :return: a live board
    """
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')


def first_player():
    """
    Randomly choose the player who goes first.
    :return: str 'player' or 'computer'
    """
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def player_chose_side():
    """
    Player chose a side he/she wants to play
    :return: a list: [player's letter , computer's letter]
    """
    letter = ''
    while not (letter == 'X' or 'O'):
        print('Choose Your side: X or O?')
        letter = input().upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def make_move(board, letter, move):
    """
    :param board: the board
    :param letter: the player's letter
    :param move: move that player choose
    :return: -
    """
    board[move] = letter


def is_winner(b, l):
    """
    Check whether the player wins
    :param b: board
    :param l: letter
    :return: True if that player has won
    """
    return ((b[1] == l and b[2] == l and b[3] == l) or # across the top
    (b[4] == l and b[5] == l and b[6] == l) or # across the middle
    (b[7] == l and b[8] == l and b[9] == l) or # across the bottom
    (b[1] == l and b[4] == l and b[7] == l) or # down the left side
    (b[2] == l and b[5] == l and b[8] == l) or # down the middle
    (b[3] == l and b[6] == l and b[3] == l) or # down the right side
    (b[7] == l and b[5] == l and b[3] == l) or # diagonal
    (b[9] == l and b[5] == l and b[1] == l)) # diagonal


def copy_board(board):
    """
    Make a duplicate of the board list
    :param board:
    :return: the duplicate
    """

    copied_board = []
    for i in board:
        copied_board.append(i)
    return copied_board


def is_space_free(board, move):

    """
    Check if the space is free or not
    :param board: the board
    :param move: the move
    :return:free space on the current board
    """
    return board[move] == ''


def get_player_move(board):

    """
    Player type his/her move
    :param board: the board
    :return: int: the move that player choose
    """
    move = ''
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not is_space_free(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


def choose_random_move(board, move_list):
    """
    Returns a valid move from the passed list on the passed board
    :param board:
    :param moves_list:
    :return:
    """
    possible_moves = []
    for i in move_list:
        if is_space_free(board, i):
            possible_moves.append(i)
        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None


def get_computer_move(board, computer_letter):
    """
    The computer decides where to move and gives his's letter on the board
    :param board: the board
    :param computer_letter: computer's letter
    :return: int the computer's move
    """
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'

    # Check if computer can win in the next move
    for i in range(1, 10):
        copy = copy_board(board)
        if is_space_free(copy, i):
            make_move(copy, computer_letter, i)
        if is_winner(copy, computer_letter):
            return i

    # Check if the player could win on their next move, and block them.

    for i in range(1, 10):
        copy = copy_board(board)
        if is_space_free(copy, i):
            make_move(copy, player_letter, i)
            if is_winner(copy, player_letter):
                return i

    # Go for the center.

    if is_space_free(board, 5):
        return 5

    # Go for the corner.

    move = choose_random_move(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Go for the sides.

    return choose_random_move(board, [2, 4, 6, 8])

def is_board_full(board):
    """
    Check if the board is already full
    :param board:
    :return: True if board is full
    """
     # Return True if every space on the board has been taken. Otherwise return False.

    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True


def restart_game():
    print('Would you like to play again? (yes or no)')
    return input().startswith('y')


while True:

    current_board = [' '] * 10
    player_letter, computer_letter = player_chose_side()
    turn = first_player()
    print('The ' + turn + ' will go first.')
    game_is_playing = True

    while game_is_playing:
        if turn == 'player':
            draw_board(current_board)
            move = get_player_move(current_board)
            make_move(current_board,player_letter,move)

            if is_winner(current_board, player_letter):
                draw_board(current_board)
                print('You win!')
                game_is_playing = False
            else:
                if is_board_full(current_board):
                    draw_board(current_board)
                    print('Game Drawn')
                    break
                else:
                    turn = 'computer'
        else:
            move = get_computer_move(current_board, computer_letter)
            make_move(current_board, computer_letter, move)

            if is_winner(current_board, computer_letter):
                draw_board(current_board)
                print('You lose')
                gameIsPlaying = False
            else:
                if is_board_full(current_board):
                    draw_board(current_board)
                    print('Game Drawn')
                    break
                else:
                    turn = 'player'

        break



