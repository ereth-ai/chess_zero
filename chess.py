#!/usr/bin/env python3
def main():
    past_moves = []
    player = WHITE
    print(LOCALIZATION[LANG]['colors'][player] + '\'s Turn:')
    board = generate_board()
    display_board(board)
    possible_moves = list_possible_moves(board, past_moves, player)
    while possible_moves:
        print(sorted(possible_moves))
        move = prompt_move()
        if not move in possible_moves:
            print('Move not possible.')
            continue
        new_board = execute_move(move, board)
        if new_board:
            board = new_board
            past_moves.append(move)
            player = BLACK if player == WHITE else WHITE
        print(LOCALIZATION[LANG]['colors'][player] + '\'s Turn:')
        display_board(board)
        possible_moves = list_possible_moves(board, past_moves, player)
        if is_in_check(board, WHITE):
            print("White King is in check")
        if is_in_check(board, BLACK):
            print("Black King is in check")
    print("CHECKMATE!")

PAWN = 0x0
KNIGHT = 0x1
BISHOP = 0x2
ROOK = 0x3
QUEEN = 0x4
KING = 0x5
EMPTY = 0x6
WHITE = 0x0
BLACK = 0x1
NOTHING = 0x2

LOCALIZATION = {
    'en':{
        'pieces':{
            PAWN:'Pawn',
            KNIGHT:'Knight',
            BISHOP:'Bishop',
            ROOK:'Rook',
            QUEEN:'Queen',
            KING:'King',
            EMPTY:'-',
        },
        'colors':{
            WHITE:'White',
            BLACK:'Black',
            NOTHING:'',
        }
    }
}

LANG = 'en'


def generate_board():
    board = []
    for i in range(8):
        row = []
        for k in range(8):
            row.append([NOTHING, EMPTY])
        board.append(row)
    for i in range(8):
        board[1][i] = [BLACK, PAWN]
        board[6][i] = [WHITE, PAWN]
    board[0][0] = [BLACK, ROOK]
    board[0][7] = [BLACK, ROOK]
    board[7][0] = [WHITE, ROOK]
    board[7][7] = [WHITE, ROOK]
    board[0][1] = [BLACK, KNIGHT]
    board[0][6] = [BLACK, KNIGHT]
    board[7][1] = [WHITE, KNIGHT]
    board[7][6] = [WHITE, KNIGHT]
    board[0][2] = [BLACK, BISHOP]
    board[0][5] = [BLACK, BISHOP]
    board[7][2] = [WHITE, BISHOP]
    board[7][5] = [WHITE, BISHOP]
    board[0][3] = [BLACK, QUEEN]
    board[7][3] = [WHITE, QUEEN]
    board[0][4] = [BLACK, KING]
    board[7][4] = [WHITE, KING]
    return board

    
def display_board(board):
    print('\t', end='')
    for i in range(8):
        print(chr(ord('a')+i)+'\t', end='')
    print()
    for i,row in enumerate(board):
        print(str(8-i)+'\t', end='')
        for cell in row:
            piece = LOCALIZATION[LANG]['pieces'][cell[1]]
            if cell[0] == WHITE:
                piece = piece.upper()
            elif cell[0] == BLACK:
                piece = piece.lower()
            print(piece+'\t',end='')
        print(str(8-i)+'\n\n', end='')
    print('\t', end='')
    for i in range(8):
        print(chr(ord('a')+i)+'\t', end='')
    print()

def list_possible_moves(board, past_moves, player=-1):
    moves = list_possible_moves_without_castling(board, player)
    if player < 0 or player == WHITE:
        if not any(e.startswith('e1') for e in past_moves):
            if not is_in_check(board, WHITE):
                # large castling
                if board[7][0][0] == WHITE and board[7][0][1] == ROOK:
                    if not any(e.startswith('a1') for e in past_moves):
                        if not is_in_check(execute_move('e1d1', board), WHITE):
                            # check collision
                            if not is_in_check(execute_move('e1c1', board), WHITE):
                                if all(board[7][e][1] == EMPTY for e in [1,2,3]):
                                    moves.append('e1c1')
                # small castling
                if board[7][7][0] == WHITE and board[7][7][1] == ROOK:
                    if not any(e.startswith('h1') for e in past_moves):
                        if not is_in_check(execute_move('e1f1', board), WHITE):
                            if not is_in_check(execute_move('e1g1', board), WHITE):
                                if all(board[7][e][1] == EMPTY for e in [5,6]):
                                    moves.append('e1g1')
    if player < 0 or player == BLACK:
        if not any(e.startswith('e8') for e in past_moves):
            if not is_in_check(board, BLACK):
                # large castling
                if board[0][0][0] == BLACK and board[0][0][1] == ROOK:
                    if not any(e.startswith('a8') for e in past_moves):
                        if not is_in_check(execute_move('e8d8', board), BLACK):
                            if not is_in_check(execute_move('e8c8', board), BLACK):
                                if all(board[0][e][1] == EMPTY for e in [1,2,3]):
                                    moves.append('e8c8')
                # small castling
                if board[0][7][0] == BLACK and board[0][7][1] == ROOK:
                    if not any(e.startswith('h8') for e in past_moves):
                        if not is_in_check(execute_move('e8f8', board), BLACK):
                            if not is_in_check(execute_move('e8g8', board), BLACK):
                                if all(board[0][e][1] == EMPTY for e in [5,6]):
                                    moves.append('e8g8')
    legal_moves = []#filter checks
    for move in moves:
        if player >=0:
            if not is_in_check(execute_move(move, board), player):
                legal_moves.append(move)
        else:
            legal_moves.append(move)
    return legal_moves
def list_possible_moves_without_castling(board, player=-1):
    # do not forget rochade and check intermittent spacefor check
    #TODO remove moves that result in check
    possible_moves = []
    for row in range(8):
        for column in range(8):
            startpos = chr(ord('a')+column)
            startpos += str(8-row)
            piece = board[row][column]
            if piece[1] == EMPTY:
                continue
            if player >= 0 and piece[0] != player:
                continue
            if piece[1] == PAWN:
                if piece[0] == WHITE:#Move up
                    # shouldn't happen since it shall convert to queen
                    if row == 0: continue 
                    if board[row-1][column][1] == EMPTY:
                        movestr = startpos + chr(ord('a')+column)
                        movestr += str(8-(row-1))
                        possible_moves.append(movestr)
                        if row == 6 and board[row-2][column][1] == EMPTY:
                            movestr = startpos + chr(ord('a')+column)
                            movestr += str(8-(row-2))
                            possible_moves.append(movestr)
                    if column > 0:
                        if board[row-1][column-1][0] == BLACK:
                            movestr = startpos+chr(ord('a')+column-1)
                            movestr += str(8-(row-1))
                            possible_moves.append(movestr)
                    if column < 7:
                        if board[row-1][column+1][0] == BLACK:
                            movestr = startpos+chr(ord('a')+column+1)
                            movestr += str(8-(row-1))
                            possible_moves.append(movestr)
                elif piece[0] == BLACK:#Move down
                    # shouldn't happen since it shall convert to queen
                    if row == 7: continue 
                    if board[row+1][column][1] == EMPTY:
                        movestr = startpos + chr(ord('a')+column)
                        movestr += str(8-(row+1))
                        possible_moves.append(movestr)
                        if row == 1 and board[row+2][column][1] == EMPTY:
                            movestr = startpos + chr(ord('a')+column)
                            movestr += str(8-(row+2))
                            possible_moves.append(movestr)
                    if column > 0:
                        if board[row+1][column-1][0] == WHITE:
                            movestr = startpos+chr(ord('a')+column-1)
                            movestr += str(8-(row+1))
                            possible_moves.append(movestr)
                    if column < 7:
                        if board[row-1][column+1][0] == WHITE:
                            movestr = startpos+chr(ord('a')+column+1)
                            movestr += str(8-(row+1))
                            possible_moves.append(movestr)
            if piece[1] == BISHOP or piece[1] == QUEEN:
                targets = []
                for i in range(1, min(row+1, column+1)):
                    target = board[row-i][column-i]
                    if target[1] == EMPTY:
                        targets.append([row-i, column-i])
                    elif target[0] != board[row][column][0]:
                        targets.append([row-i, column-i])
                        break
                    else:
                        break
                for i in range(1, min(row+1, 8-column)):
                    target = board[row-i][column+i]
                    if target[1] == EMPTY:
                        targets.append([row-i, column+i])
                    elif target[0] != board[row][column][0]:
                        targets.append([row-i, column+i])
                        break
                    else:
                        break
                for i in range(1, min(8-row, column+1)):
                    target = board[row+i][column-i]
                    if target[1] == EMPTY:
                        targets.append([row+i, column-i])
                    elif target[0] != board[row][column][0]:
                        targets.append([row+i, column-i])
                        break
                    else:
                        break
                for i in range(1, min(8-row, 8-column)):
                    target = board[row+i][column+i]
                    if target[1] == EMPTY:
                        targets.append([row+i, column+i])
                    elif target[0] != board[row][column][0]:
                        targets.append([row+i, column+i])
                        break
                    else:
                        break
                for target in targets:
                    movestring = startpos + chr(ord('a')+target[1]) + str(8-target[0])
                    possible_moves.append(movestring)
            if piece[1] == ROOK or piece[1] == QUEEN:
                for i in range(1, row+1):
                    if board[row-i][column][1] == EMPTY:
                        movestr = startpos+chr(ord('a')+column)
                        movestr += str(8-(row-i))
                        possible_moves.append(movestr)
                    elif board[row-i][column][0] != board[row][column][0]:
                        movestr = startpos+chr(ord('a')+column)
                        movestr += str(8-(row-i))
                        possible_moves.append(movestr)
                        break
                    else:
                        break
                for i in range(1, 8-row):
                    if board[row+i][column][1] == EMPTY:
                        movestr = startpos+chr(ord('a')+column)
                        movestr += str(8-(row+i))
                        possible_moves.append(movestr)
                    elif board[row+i][column][0] != board[row][column][0]:
                        movestr = startpos+chr(ord('a')+column)
                        movestr += str(8-(row+i))
                        possible_moves.append(movestr)
                        break
                    else:
                        break
                for i in range(1, 8-column):
                    if board[row][column+i][1] == EMPTY:
                        movestr = startpos+chr(ord('a')+column+i)
                        movestr += str(8-row)
                        possible_moves.append(movestr)
                    elif board[row][column+i][0] != board[row][column][0]:
                        movestr = startpos+chr(ord('a')+column+i)
                        movestr += str(8-row)
                        possible_moves.append(movestr)
                        break
                    else:
                        break
                for i in range(1, column+1):
                    if board[row][column-i][1] == EMPTY:
                        movestr = startpos+chr(ord('a')+column-i)
                        movestr += str(8-row)
                        possible_moves.append(movestr)
                    elif board[row][column-i][0] != board[row][column][0]:
                        movestr = startpos+chr(ord('a')+column-i)
                        movestr += str(8-row)
                        possible_moves.append(movestr)
                        break
                    else:
                        break
            if piece[1] == KNIGHT:
                targets = []
                if 0<=row+2<=7 and 0<=column+1<=7:
                    target_coord = board[row+2][column+1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+2,column+1])
                if 0<=row+2<=7 and 0<=column-1<=7:
                    target_coord = board[row+2][column-1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+2,column-1])
                if 0<=row-2<=7 and 0<=column+1<=7:
                    target_coord = board[row-2][column+1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-2,column+1])
                if 0<=row-2<=7 and 0<=column-1<=7:
                    target_coord = board[row-2][column-1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-2,column-1])
                if 0<=row+1<=7 and 0<=column+2<=7:
                    target_coord = board[row+1][column+2]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+1,column+2])
                if 0<=row+1<=7 and 0<=column-2<=7:
                    target_coord = board[row+1][column-2]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+1,column-2])
                if 0<=row-1<=7 and 0<=column+2<=7:
                    target_coord = board[row-1][column+2]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-1,column+2])
                if 0<=row-1<=7 and 0<=column-2<=7:
                    target_coord = board[row-1][column-2]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-1,column-2])
                for target in targets:
                    movestring = startpos + chr(ord('a')+target[1]) + str(8-target[0])
                    possible_moves.append(movestring)
            if piece[1] == KING:
                targets = []
                if 0<=row+1<=7 and 0<=column+1<=7:
                    target_coord = board[row+1][column+1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+1,column+1])
                if 0<=row+1<=7 and 0<=column-1<=7:
                    target_coord = board[row+1][column-1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+1,column-1])
                if 0<=row+1<=7 and 0<=column<=7:
                    target_coord = board[row+1][column]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row+1,column])
                if 0<=row-1<=7 and 0<=column+1<=7:
                    target_coord = board[row-1][column+1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-1,column+1])
                if 0<=row-1<=7 and 0<=column-1<=7:
                    target_coord = board[row-1][column-1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-1,column-1])
                if 0<=row-1<=7 and 0<=column<=7:
                    target_coord = board[row-1][column]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row-1,column])
                if 0<=row<=7 and 0<=column+1<=7:
                    target_coord = board[row][column+1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row,column+1])
                if 0<=row<=7 and 0<=column-1<=7:
                    target_coord = board[row][column-1]
                    if target_coord[1] == EMPTY or target_coord[0] != board[row][column][0]:
                        targets.append([row,column-1])
                for target in targets:
                    movestring = startpos + chr(ord('a')+target[1]) + str(8-target[0])
                    possible_moves.append(movestring)
    return possible_moves

def prompt_move():
    move = input('Next move: ')
    return move

def execute_move(move, master_board):
    board = []
    for row in master_board:
        row_copy = []
        for cell in row:
            row_copy.append(cell[::])
        board.append(row_copy)

    try:
        assert len(move)==4
        column_start = ord(move[0])-ord('a')
        row_start = 8-int(move[1])
        column_end = ord(move[2])-ord('a')
        row_end = 8-int(move[3])
        assert 0<=column_start<=7
        assert 0<=row_start<=7
        assert 0<=column_end<=7
        assert 0<=row_end<=7

        if move == 'e1g1':
            if board[7][4][1] == KING:
                board = execute_move('h1f1', board)
        if move == 'e1c1':
            if board[7][4][1] == KING:
                board = execute_move('a1d1', board)
        if move == 'e8g8':
            if board[0][4][1] == KING:
                board = execute_move('h8f8', board)
        if move == 'e8c8':
            if board[0][4][1] == KING:
                board = execute_move('a8d8', board)

        board[row_end][column_end] = board[row_start][column_start]
        board[row_start][column_start] = [NOTHING, EMPTY]
        if move.endswith('8') or move.endswith('1'):
            if board[row_end][column_end][1] == PAWN:
                board[row_end][column_end][1] = QUEEN
    except (AssertionError, ValueError):
        print('Invalid move:', move)
        return None
    return board

def is_in_check(board, player):
    if not board: return False
    for row in range(8):
        for column in range(8):
            if board[row][column][1] != KING: continue
            if board[row][column][0] == player:
                possible_moves = list_possible_moves_without_castling(board)
                if any(e.endswith(chr(ord('a')+column)+str(8-row)) for e in possible_moves):
                    return True
                else:
                    return False

if __name__ == '__main__':
    main()
