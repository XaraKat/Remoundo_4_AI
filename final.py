import numpy as np
import pygame
import sys
import math
import random

#xromata
PINK = (255,204,229)
RED = (102,0,51)
YELLOW = (255,255,153)
BLUE = (102,102,255)

#sires tou paixnidiou
PLAYER_TURN = 0
AI_TURN = 1

#sinolo row kai col
ROW_SUM = 6
COLUMN_SUM = 7

#dimiourgia tou pinaka
def create_board():
	#to board 3ekinai me midenika
	board = np.zeros((ROW_SUM,COLUMN_SUM))
	return board

#tosopothetisi pioniou ston pinaka
def place_piece(board, row, col, piece):
	board[row][col] = piece

#epalithithefsi eleftheris thesis
def free_space(board, col):
	return board[ROW_SUM-1][col] == 0

#gia na topothetithi to pioni sto sosto row
def open_row(board, col):
	for i in range(ROW_SUM):
		if board[i][col] == 0:
			return i

#kanei emfanisi tou board anapoda oste na emfanizonte sosta
def show_board(board):
	print(np.flip(board, 0))

#oi dinami ton kiniseon tou ai 
def evaluate(window, piece):
	s = 0
	rival = 1
	if piece == 1:
		rival = 2
	
	#to count kanei store	
	if window.count(piece) == 3 and window.count(0) == 1:
		s += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		s += 2
	if window.count(rival) == 3 and window.count(0) == 1:
		s -= 4
		
	return s

#pernoume ta kena koutia tou board
def get_free_spaces(board):
	free_scapes_list = [] 
	for col in range(COLUMN_SUM):
		if free_space(board, col):
			free_scapes_list.append(col)
	
	return free_scapes_list


def termi_node(board):
	#epistrefi true ean exei kerdisi o paiktis/ to ai / exei gemisi to board alios false
	return winner(board, 1) or winner(board, 2) or len(get_free_spaces(board)) == 0

#min max algorithmos
def min_max(board, depth, maximizingPlayer):

	free_spaces = get_free_spaces(board)
	terminal_node = termi_node(board)
	if depth == 0 or terminal_node: 
		if depth == 0:
			return (None, check_for_winner(board, 2))
		else:
			#pioni paixti
			if winner(board, 1): 
				return (None, -10000000)
			#pioni ai
			elif winner(board, 2):
				return (None, 10000000)
			#den exi elefthera koutia
			else:
				return (None, 0)
				
	if maximizingPlayer:
		#arnitiko apiro
		value = -math.inf		
		best_col = 1
		for col in free_spaces:
			row = open_row(board, col)
			board_copy = board.copy()
			place_piece(board_copy, row, col, 2)
			value2 = min_max(board_copy, depth-1, False)[1]
			if value2 > value:
				value = value2
				best_col = col
		return best_col, value
			
	else: 	#minimizing player
		#thetiko apiro
		value = math.inf		
		best_col = 1
		for col in free_spaces:
			row = open_row(board, col)
			board_copy = board.copy()
			place_piece(board_copy, row, col, 1)
			value2 = min_max(board_copy, depth-1, True)[1]
			if value2 < value:
				value = value2
				best_col = col
		return best_col, value
	

def AIs_move(board, piece):	
	free_scapes_list = get_free_spaces(board)
	best_s = 0
	best_col = random.choice(free_scapes_list)
	for col in free_scapes_list:
		row = open_row(board, col)
		t_b = board.copy()
		place_piece(t_b, row, col, piece)
		s = check_for_winner(t_b, piece)
		
		if s > best_s: 
			best_s = s 
			best_col = col 
	
	return best_col

#elegxos gia to ean exei kerdsi kapoios
def winner(board, piece):

	#elegxoume ta column prota
	for j in range(COLUMN_SUM-3):
		for i in range(ROW_SUM):
			#ean tessera pionia stin sira tote epistrefei TRUE
			if board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece:
				return True

	#elegxoume gia katheta
	for j in range(COLUMN_SUM):
		for i in range(ROW_SUM-3):
			#ean tessera pionia stin sira tote epistrefei TRUE
			if board[i][j] == piece and board[i+1][j] == piece and board[i+2][j] == piece and board[i+3][j] == piece:
				return True

	#elegxos gia de3ia diagonio
	for j in range(COLUMN_SUM-3):
		for i in range(ROW_SUM-3):
			if board[i][j] == piece and board[i+1][j+1] == piece and board[i+2][j+2] == piece and board[i+3][j+3] == piece:
				return True

	#elegxos gia aristera diagonio
	for j in range(COLUMN_SUM-3):
		for i in range(3, ROW_SUM):
			if board[i][j] == piece and board[i-1][j+1] == piece and board[i-2][j+2] == piece and board[i-3][j+3] == piece:
				return True

	
#dinates epiloges gia niki	
def check_for_winner(board, piece):
	s = 0 
	array1 = [int(i) for i in list(board[:, COLUMN_SUM//2])]
	sum = array1.count(piece)
	s += sum*3
	
	#orizontia
	for i in range(ROW_SUM):
		row_array = [int(j) for j in list(board[i,:])]
		for w in range(COLUMN_SUM-3):
			window = row_array[w:w+4]
			
			s += evaluate(window, piece)	
	#katheta 
	for i in range(COLUMN_SUM):
		col_array = [int(j) for j in list(board[:, i])]
		for w in range(ROW_SUM-3):
			window = col_array[w:w+4]
			
			s += evaluate(window, piece)
	
	#de3ia diagonios
	for i in range(ROW_SUM-3):
		for j in range(COLUMN_SUM-3):
			window = [board[i+w][j+w] for w in range(4)]
			
			s += evaluate(window, piece)
				
	#aristera diagonios
	for i in range(ROW_SUM-3):
		for j in range(COLUMN_SUM-3):
			window = [board[i+3-w][j+w] for w in range(4)]
		
			s += evaluate(window, piece)
			
	return s


#sxediasmos board
def draw_board(board):
	for j in range(COLUMN_SUM):
		for i in range(ROW_SUM):
			pygame.draw.rect(screen, RED, (j*no_of_pixel, i*no_of_pixel+no_of_pixel, no_of_pixel, no_of_pixel))
			pygame.draw.circle(screen, PINK, (int(j*no_of_pixel+no_of_pixel/2), int(i*no_of_pixel+no_of_pixel+no_of_pixel/2)), RADIUS)
	
	for j in range(COLUMN_SUM):
		for i in range(ROW_SUM):		
			if board[i][j] == 1:
				pygame.draw.circle(screen, BLUE, (int(j*no_of_pixel+no_of_pixel/2), height-int(i*no_of_pixel+no_of_pixel/2)), RADIUS)
			elif board[i][j] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(j*no_of_pixel+no_of_pixel/2), height-int(i*no_of_pixel+no_of_pixel/2)), RADIUS)
	pygame.display.update()


board = create_board()
show_board(board)
game_over = False
turn = 0

pygame.init()

#to paixnidi mas tha einai se 100 pixel
no_of_pixel = 80

#i vasi tha einai isi me ta column pou exoume 
base = COLUMN_SUM * no_of_pixel

#to ipsos tha exi +1 gia na vlepoume pou theloume na ri3oume to pioni  
height = (ROW_SUM+1) * no_of_pixel

size = (base, height)

#rithmizoume to radious sto miso gia na emfanizi kiklous to board
RADIUS = int(no_of_pixel/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

#oso iparxoun kinisis i dn exei kerdisi kapoios
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		#otan kouniete to mouse kouniete kai o kiklos mazi
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, PINK, (0,0, base, no_of_pixel))
			posx = event.pos[0]
			if turn == PLAYER_TURN:
				pygame.draw.circle(screen, BLUE, (posx, int(no_of_pixel/2)), RADIUS) 
		pygame.display.update()

		#otan patame to mouse
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, PINK, (0,0, base, no_of_pixel))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER_TURN:
				posx = event.pos[0]
				col = int(math.floor(posx/no_of_pixel))

				if free_space(board, col):
					row = open_row(board, col)
					place_piece(board, row, col, 1)

					if winner(board, 1):
						label = myfont.render("Player wins!", 1, BLUE)
						screen.blit(label, (100,10))
						game_over = True

					turn += 1
					turn = turn % 2

					show_board(board)
					draw_board(board)
		
	#kinisi ai
	if turn == AI_TURN and not game_over:		 

		col, minimax_score = min_max(board, 4, True)
		
		if free_space(board, col):
			
			row = open_row(board, col)
			place_piece(board, row, col, 2)

		if winner(board, 2):
			label = myfont.render("AI wins!", 1, YELLOW)
			screen.blit(label, (170,10))
			game_over = True

		#500ms mexri na di3i tin kinisi tou AI
		pygame.time.wait(500)
		show_board(board)
		draw_board(board)

		turn += 1
		turn = turn % 2

		if game_over:
			pygame.time.wait(3000)
			
