import pygame, os, sys, string
from pygame.locals import *
from random import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

#            R    G    B
GRAY     = (210, 210, 210)
NAVYBLUE = ( 60,  60, 100)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
WHITE    = (255, 255, 255)
BROWN    = (139,  69,  42)
WHEAT    = (238, 213, 183)
SMOKE    = (245, 245, 245)
BLACK    = (  0,   0,   0)
OLIVE    = ( 85, 107,  47)
LIME     = ( 50, 205,  50)

########## STARTING POSITIONS

# piece[X,Y]


positions = {

'black_pawn0'   : [0, 1],
'black_pawn1'   : [1, 1],
'black_pawn2'   : [2, 1],
'black_pawn3'   : [3, 1],
'black_pawn4'   : [4, 1],
'black_pawn5'   : [5, 1],
'black_pawn6'   : [6, 1],
'black_pawn7'   : [7, 1],

'white_pawn0'   : [0, 6],
'white_pawn1'   : [1, 6],
'white_pawn2'   : [2, 6],
'white_pawn3'   : [3, 6],
'white_pawn4'   : [4, 6],
'white_pawn5'   : [5, 6],
'white_pawn6'   : [6, 6],
'white_pawn7'   : [7, 6],

'black_rook0'   : [0,0],
'black_rook1'   : [7, 0],

'white_rook0'   : [0, 7],
'white_rook1'   : [7, 7],

'black_knight0' : [1, 0],
'black_knight1' : [6, 0],

'white_knight0' : [1, 7],
'white_knight1' : [6, 7],

'black_bishop0' : [2, 0],
'black_bishop1' : [5, 0],

'white_bishop0' : [2, 7],
'white_bishop1' : [5, 7],

'black_queen0'  : [3, 0],
'white_queen0'  : [3, 7],

'black_king0'   : [4, 0],
'white_king0'   : [4, 7]

}


def half(x): return x / 2.


###########################################################

size = (1100, 800)

side = 5 * min(size) / 6

board_size = tuple([side] * 2)

# Board dimensions
width = board_size[0] / 8
height = board_size[1] / 8


# Top left coord of the board
x_i = (size[0] - board_size[0]) / 8
y_i = (size[1] - board_size[1]) / 4



### PIECES
scale = 30


h_scale = half(scale)

# Main screen
screen = pygame.display.set_mode(size)

# Add icon
pygame.display.set_icon(pygame.image.load('Pieces/Icon.png'))

# Clear caption
pygame.display.set_caption("")

screen.fill(SMOKE)


# Pieces surface
psrf = pygame.Surface(board_size, pygame.SRCALPHA, 32)
psrf = psrf.convert_alpha()



pygame.font.init()
clock = pygame.time.Clock()
FPS = 20


###########################################################



class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Pieces/' + typ[:-1] + '.png')
        self.image = pygame.transform.scale(self.image, (int(width - scale), int(height - scale)))
        self.id = typ

        self.x = 0
        self.y = 0
        
        self.selected = False

    def move(self, new_pos):
        self.x = new_pos[0]
        self.y = new_pos[1]

    def update(self):
        if on_board(self.id):
            psrf.blit(self.image, (self.x, self.y))








black_pieces = pygame.sprite.Group()
white_pieces = pygame.sprite.Group()

active_pieces = pygame.sprite.Group()

for piece in positions:
    p = ChessPiece(piece)

    if 'black' in piece:
        black_pieces.add(p)
    else:
        white_pieces.add(p)

    active_pieces.add(p)










# Positions to place pieces
pos = {}


# Add the squares of the board
y = 0
for i in xrange(8):
    x = 0
    for j in xrange(8):
        col = BROWN if (i%2 == j%2) else WHEAT
        pygame.draw.rect(psrf, col, (x, y, width + 1, height + 1))
        pos[str(j)+str(i)] = (x + h_scale, y + h_scale)
        x += width
    y += height

# Outline the board
t = 2       # Line thickness
shift = 0   # Used so all lines show
for k in xrange(9):
    pygame.draw.line(psrf, BLACK, [0, (height * k) - shift], [board_size[0], (height * k) - shift], t)
    pygame.draw.line(psrf, BLACK, [(width * k) - shift, 0], [(width * k) - shift, board_size[1],], t)
    shift = 0 if k != 8 else 1

# Board Surface
board = psrf.copy()



# Add letters and numbers
bot = y + half(height) + 10
side = x_i - 20
font = pygame.font.Font(None, 23)
for i in xrange(8):
    let = font.render(string.uppercase[i], True, BLACK)
    num = font.render(str(8 - i), True, BLACK)

    screen.blit(let, (x_i + half(width) + (i * width) - 2, bot))
    screen.blit(num, (side, y_i + half(height) + (i * height)))



def on_board(id):
    """
        Makes sure position is on the board
    """

    po = positions[id]
    if (-1 < po[0] < 8) and (-1 < po[1] < 8):
        return True
    else:
        return False



def read_id(id):
    """
        Turns integer list into string
    """

    return ''.join([str(i) for i in positions[id]])



def reset_board():
    """
        Places pieces in initial
        positions
    """

    psrf.blit(board, (0, 0))
    for p in active_pieces:
        if on_board(p.id):
            p.move(pos[read_id(p.id)])

    active_pieces.update()
    screen.blit(psrf, (x_i, y_i))


# MOVES #
##############################################################################



def pawn_moves(start):
    """
        Allowable pawn moves based
        on position
    """

    places = []
    sign = -1 if move[0] == 'white' else 1
    n = 3 if ([start[1], move[0]] == [6, 'white']) or ([start[1], move[0]] == [1, 'black'])  else 2
    for i in xrange(1, n):
        if [start[0], start[1] + (sign * i)] in positions.values():
            break
        else:
            places.append([start[0], start[1] + (sign * i)])

    for en in positions:
        if move[1] in en:
            if [abs(z - q) for z, q in zip(start, positions[en])] == [1, 1]:
                places.append(positions[en])

    return places



def knight_moves(start):
    """
        Allowable knight moves based
        on position
    """

    places = []
    for dx in range(8):
        for dy in range(8):
            checkx, checky = [abs(n - start[ind]) for ind, n in enumerate([dx, dy])]
            if checkx and checky and (checkx + checky == 3):
                for block in positions:
                    if move[0] in block and positions[block] == [dx, dy]:
                        break
                else:
                    places.append([dx, dy])

    return places



def king_moves(start):
    """
        Allowable king moves based
        on position
    """

    places = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            test_pos = [sum(v) for v in zip(start, [i, j])]
            if not (i == 0 and j == 0) and (-1 not in test_pos) and (8 not in test_pos):
                if test_pos not in positions.values():
                    places.append(test_pos)
                else:
                    for p in positions:
                        if positions[p] == test_pos and move[1] in p:
                            places.append(test_pos)

    return places



def vertical_moves(start):
    """
        Determines distance a piece can 
        move horizontally or vertically
    """

    places = []
    for ind in xrange(2):
        for ran in [xrange(start[ind] + 1, 8), xrange(start[ind] - 1, -1, -1)]:
            b = 0
            for m in ran:
                check = [start[0], m] if ind else [m, start[1]]  
                if b:
                    break
                if check not in positions.values():
                    places.append(check)
                else:
                    for q in positions:
                        if positions[q] == check:
                            if move[1] in q:
                                places.append(check)
                            b = 1
                            break

    return places



def diagonal_moves(start):
    """
        Determines distance a piece can 
        move diagonally
    """

    places = []
    signs = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    for s in signs:
        test_pos = [sum(i) for i in zip(start, s)]
        b = 0
        while (not b) and (-1 not in test_pos) and (8 not in test_pos):
            if test_pos not in positions.values():
                places.append(test_pos)
            else:
                b = 1
                for p in positions:
                    if positions[p] == test_pos and move[1] in p:
                        places.append(test_pos)

            test_pos = [sum(i) for i in zip(test_pos, s)]

    return places



##############################################################################


def can_move(spot):
    """
        Wrapped function to determine where
        selected piece can legally move
    """

    places = []
    for p in positions:
        if pos[read_id(p)] == spot:
            start = positions[p]
            if move[0] in p:

                if 'pawn' in p:
                    places += pawn_moves(start)

                if 'rook' in p:
                    places += vertical_moves(start)

                if 'knight' in p:
                    places += knight_moves(start)

                if 'bishop' in p:
                    places += diagonal_moves(start)

                if 'queen' in p:
                    places += vertical_moves(start)
                    places += diagonal_moves(start)

                if 'king' in p:
                    places += king_moves(start)


    if places:
        return LIME, places
    else:
        return RED, places



def remove(enemy):
    """
        Removes enemy piece
        when it is taken
    """

    positions.pop(enemy)
    for piece in active_pieces:
        if piece.id == enemy:
            piece.kill()


            
def mouse_pos(click_pos):
    """
        Determines the position chosen based
        on the mouse
    """

    cx, cy = click_pos
    if (x_i < cx < (x_i + board_size[0])) and (y_i < cy < (y_i + board_size[1])):
        xp = yp = 0
        for i in act_pos:
            if xp < act_pos[i][0] < cx:
                xp = act_pos[i][0]
            if yp < act_pos[i][1] < cy:
                yp = act_pos[i][1]

        try:
            return [act_pos[i] for i in act_pos if act_pos[i] == [xp, yp]][0]
        except:
            pass

    return [0, 0]



move_font = pygame.font.Font(None, 30)

act_pos = pos.copy()

for p in act_pos:
    act_pos[p] = list(act_pos[p])
    act_pos[p][0] += x_i
    act_pos[p][1] += y_i

hl_x, hl_y = act_pos['07']

reset_board()   
pygame.display.update()

selected = False
box = RED

move = ['white', 'black']

# Backgroun surface
background = pygame.image.load('Pieces/wood.jpg')
background = pygame.transform.scale(background, size)

# Turn Display
turn = pygame.Surface((board_size[0], half(size[1] - board_size[1]) - scale))

# Options Display
options = pygame.Surface((size[0] - board_size[0] - x_i - (5 * x_i / 4), board_size[1] + 3 * half(turn.get_height()))) 

hover = True
old_mx, old_my = [0, 0]

sel_piece = ''
while 1:

    clicked = False
    enter = False

    mp_x, mp_y = pygame.mouse.get_pos()

    if hover:
        if x_i <= mp_x <= (x_i + board_size[0]) and y_i <= mp_y <= (y_i + board_size[1]):
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if hover:
            mp_x, mp_y = mouse_pos((mp_x, mp_y))
            if [mp_x, mp_y] == [old_mx, old_my]:
                mp_x = mp_y = 0
            else:
                old_mx, old_my = mp_x, mp_y
            

            if mp_x and mp_y:
                hl_x, hl_y = mp_x, mp_y

        if event.type == MOUSEBUTTONDOWN:
            
            mp_x, mp_y = mouse_pos((mp_x, mp_y))

            if mp_x and mp_y:
                hl_x, hl_y = mp_x, mp_y

            if box == LIME or box == YELLOW:
                enter = True

            clicked = True

        if event.type == KEYUP and not clicked:

            if event.key == K_UP and hl_y > y_i + h_scale:
                hl_y -= height

            if event.key == K_DOWN and hl_y + h_scale < y_i + board_size[1] - height:
                hl_y += height
                
            if event.key == K_LEFT and hl_x > x_i + h_scale:
                hl_x -= width

            if event.key == K_RIGHT and hl_x + h_scale < x_i + board_size[0] - width:
                hl_x += width

            if (event.key == K_RETURN or event.key == K_SPACE) and (box == LIME or box == YELLOW):
                enter = True

    if enter:
        if not selected:
            selx = hl_x
            sely = hl_y
            for piece in active_pieces:
                if [piece.x, piece.y] == [hl_x - x_i, hl_y - y_i]:
                    sel_piece = piece.id
                    break
            box = YELLOW
        else:
            for p in act_pos:
                if act_pos[p] == [hl_x, hl_y]:
                    move_to = [int(i) for i in p]
                    break
            if move_to in places:
                for piece in active_pieces:
                    if piece.id == sel_piece:
                        piece.move([hl_x - x_i, hl_y - y_i])
                        for en in positions:
                            if positions[en] == move_to:
                                remove(en)
                                break
                        positions[piece.id] = move_to
                        move.reverse()
                        break
        selected = True if not selected else False
        if not selected:
            sel_piece = ''




    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # If piece isn't selected, determine if highlighting box contains piece that can move
    if not selected:
        box, places = can_move((hl_x - x_i, hl_y - y_i))

    # Add background
    screen.blit(background, (0, 0))

    # Add stats & options display
    options.fill(WHEAT)
    pygame.draw.rect(options, BLACK, (0, 0, options.get_width(), options.get_height()), 1)
    screen.blit(options, ((x_i + board_size[0] + half(x_i), y_i)))

    # Add board
    psrf.blit(board, (0, 0))

    # Update pieces
    active_pieces.update()

    # Add pieces to board
    screen.blit(psrf , (x_i, y_i))

    # Add turn display
    text = move_font.render("Turn:  " + move[0].title(), True, BLACK)
    turn.fill(WHEAT)
    pygame.draw.rect(turn, BLACK, (0, 0, turn.get_width(), turn.get_height()), 1)
    turn.blit(text, (half(turn.get_width() - text.get_width()), half(turn.get_height() - text.get_height())))
    screen.blit(turn, (x_i, y_i + board_size[1] + half(turn.get_height())))

    # Add box around piece that is selected
    if selected:
        pygame.draw.rect(screen, LIME, (selx - h_scale, sely - h_scale, width, height), 4)

    # Add highlighting box
    pygame.draw.rect(screen, box, (hl_x - h_scale, hl_y - h_scale, width, height), 4)



    if places:
        for h in places:
            xy = pos[''.join([str(i) for i in h])]
            hsrf = pygame.Surface((width, height))
            hsrf.fill(YELLOW)
            hsrf.set_alpha(70)
            screen.blit(hsrf, [j1 + j2 for j1, j2 in zip(xy, [x_i - h_scale, y_i - h_scale])])


    pygame.display.update()
    clock.tick(FPS)