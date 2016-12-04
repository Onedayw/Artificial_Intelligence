# f = open("./TestCasesHW2/Test10/input.txt", "r")
f = open("input.txt", "r")
# f = open("input5.txt", "r")

lines = f.readlines()

N = int(lines[0].strip('\r\n'))
Mode = str(lines[1].strip('\r\n'))
PlayerA = str(lines[2].strip('\r\n'))
PlayerB = "X"
if PlayerA == "X":
    PlayerB = "O"
Depth = int(lines[3].strip('\r\n'))

alph = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
        7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N',
        14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
        21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

resource = {}
cur_board = {}

for i in range(4, 4 + N):
    lines[i] = lines[i].strip('\r\n')
    rowlist = lines[i].split()
    row = i - 4
    resource[row] = {}
    for j in range(0, N):
        resource[row][j] = int(rowlist[j])

for i in range(4 + N, len(lines)):
    lines[i] = lines[i].strip('\r\n')
    rowlist = lines[i]
    row = i - (4 + N)
    cur_board[row] = {}
    for j in range(0, N):
        cur_board[row][j] = rowlist[j]

def boardisfull(board):
    cnt = 0
    for i in range(0, N):
        for j in range(0, N):
            if board[i][j] == ".":
                cnt = cnt + 1
    return cnt == 0


def Total_Score(board):
    scoreA = 0
    scoreB = 0
    for i in range(0, N):
        for j in range(0, N):
            if (board[i][j] == PlayerA):
                scoreA = scoreA + resource[i][j]
            elif (board[i][j] == PlayerB):
                scoreB = scoreB + resource[i][j]
    return scoreA - scoreB


def Get_Position(row, col):
    return alph[col] + str(row + 1)


def Get_Move_Type(state, i, j, player):
    # stake
    player2 = ""
    if player == "X":
        # 1: X 2: O
        player2 = "O"
    else:
        # 1: O 2: X
        player2 = "X"
    # top
    if (i - 1 >= 0 and state[i - 1][j] == player):
        if (i + 1 < N and state[i + 1][j] == player2):
            return "Raid"
        if (j - 1 >= 0 and state[i][j - 1] == player2):
            return "Raid"
        if (j + 1 < N and state[i][j + 1] == player2):
            return "Raid"
    # bottom
    if (i + 1 < N and state[i + 1][j] == player):
        if (i - 1 >= 0 and state[i - 1][j] == player2):
            return "Raid"
        if (j - 1 >= 0 and state[i][j - 1] == player2):
            return "Raid"
        if (j + 1 < N and state[i][j + 1] == player2):
            return "Raid"
    # left
    if (j - 1 >= 0 and state[i][j - 1] == player):
        if (i + 1 < N and state[i + 1][j] == player2):
            return "Raid"
        if (i - 1 >= 0 and state[i - 1][j] == player2):
            return "Raid"
        if (j + 1 < N and state[i][j + 1] == player2):
            return "Raid"
    # right
    if (j + 1 < N and state[i][j + 1] == player):
        if (i + 1 < N and state[i + 1][j] == player2):
            return "Raid"
        if (i - 1 >= 0 and state[i - 1][j] == player2):
            return "Raid"
        if (j - 1 >= 0 and state[i][j - 1] == player2):
            return "Raid"
    return "Stake"

def Get_Next_State(state, i, j, player):
    new_board = {}
    player2 = ""
    if (player == "X"):
        player2 = "O"
    else:
        player2 = "X"
    if (Get_Move_Type(state, i, j, player) == "Stake"):
        for row in range(0, N):
            new_board[row] = {}
            for col in range(0, N):
                new_board[row][col] = state[row][col]
                if (i == row and j == col):
                    # print "dd"
                    new_board[i][j] = player
    else:
        # Raid
        for row in range(0, N):
            new_board[row] = {}
            for col in range(0, N):
                new_board[row][col] = state[row][col]
                if (i == row and j == col):
                	new_board[i][j] = player
                # check around have player2 or not
                square = new_board[row][col]
                if (square == player2 and row == i and col == j - 1):
                    new_board[row][col] = player
                if (square == player2 and row == i and col == j + 1):
                    new_board[row][col] = player
                if (square == player2 and row == i + 1 and col == j):
                    new_board[row][col] = player
                if (square == player2 and row == i - 1 and col == j):
                    new_board[row][col] = player

    return new_board

def Get_Next_Stake_State(state, i, j, player):
	new_board = {}
	for row in range (N):
		new_board[row] = {}
		for col in range (N):
			new_board[row][col] = state[row][col]
			if(i == row and j == col):
				new_board[i][j] = player
	return new_board

def Get_Final_board(state, i, j, player, move_type):
	new_board = {}
	player2 = ""
	if (player == "X"):
		player2 = "O"
	else:
		player2 = "X"
	if(move_type == "Stake"):
		for row in range(0, N):
			new_board[row] = {}
			for col in range(0, N):
				new_board[row][col] = state[row][col]
				if (i == row and j == col):
					new_board[i][j] = player

	if(move_type == "Raid"):
		for row in range(0, N):
			new_board[row] = {}
			for col in range(0, N):
				new_board[row][col] = state[row][col]
				if (i == row and j == col):
					new_board[i][j] = player
				 # check around have player2 or not
				square = new_board[row][col]
				if (square == player2 and row == i and col == j - 1):
					new_board[row][col] = player
				if (square == player2 and row == i and col == j + 1):
					new_board[row][col] = player
				if (square == player2 and row == i + 1 and col == j):
					new_board[row][col] = player
				if (square == player2 and row == i - 1 and col == j):
					new_board[row][col] = player
	return new_board

def Minimax_Search(state, cur_depth, max_depth, player, position):
    if (cur_depth >= max_depth or boardisfull(state)):
        return Total_Score(state)
    cur_position = ""
    cur_type = ""
    if (player == PlayerA):
        v = float('-inf')
        for i in range(0, N):
            for j in range(0, N):
                if (state[i][j] == "X" or state[i][j] == "O"):
                    continue
                # ----------------
                # new_board = Get_Next_Stake_State(state, i, j, player)
                # cur_val = Minimax_Search(new_board, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))
                state[i][j]=player
                cur_val = Minimax_Search(state, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))
                state[i][j]="."

                if (cur_val == v and Get_Move_Type(state, i, j, player) != "Stake" ):
                	cur_type = "Stake"
                	cur_position = [Get_Position(i, j), i, j, cur_type]
                if (cur_val > v):
                	v = cur_val
                	cur_type = "Stake"
                	cur_position = [Get_Position(i, j), i, j, cur_type]

                v = max(v, cur_val)
	            # --------------
                new_board = Get_Next_State(state, i, j, player)
                cur_val = Minimax_Search(new_board, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))

                if (cur_val == v and cur_type == "Raid"):
                    if Get_Move_Type(state, i, j, player) == "Stake":
                    	cur_type = Get_Move_Type(state, i, j, player)
                        cur_position = [Get_Position(i, j), i, j, cur_type]
                        
                if (cur_val > v):
                    # replace
                    v = cur_val
                    cur_type = Get_Move_Type(state, i, j, player)
                    cur_position = [Get_Position(i, j), i, j, cur_type]

        if (position == "start"):
            return cur_position
        return v
    else:
        v = float('inf')
        for i in range(0, N):
            for j in range(0, N):
                if (state[i][j] == "X" or state[i][j] == "O"):
                    continue
                new_board = Get_Next_State(state, i, j, player)
                cur_val = Minimax_Search(new_board, cur_depth + 1, Depth, PlayerA, Get_Position(i, j))
                v = min(v, cur_val)
        return v

def Alpha_Beta_Search(state, alpha, beta, cur_depth, max_depth, player, position):
    if (cur_depth >= max_depth or boardisfull(state)):
        return Total_Score(state)
    cur_position = ""
    cur_type = ""
    if (player == PlayerA):
        v = float('-inf')
        for i in range(0, N):
            for j in range(0, N):
                if state[i][j] == ".":
                	# ----------------
                	# new_board = Get_Next_Stake_State(state, i, j, player)
	                # cur_val = Alpha_Beta_Search(new_board, alpha, beta, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))
	                state[i][j]=player
	                cur_val = Alpha_Beta_Search(state, alpha, beta, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))
	                state[i][j]="."

	                if (cur_val == v and Get_Move_Type(state, i, j, player) != "Stake" ):
						cur_type = "Stake"
						cur_position = [Get_Position(i, j), i, j, cur_type]

	                if (cur_val > v):
	                    v = cur_val
	                    cur_type = "Stake"
	                    cur_position = [Get_Position(i, j), i, j, cur_type]

	                v = max(v, cur_val)
	                # --------------

	                new_board = Get_Next_State(state, i, j, player)
	                cur_val = Alpha_Beta_Search(new_board, alpha, beta, cur_depth + 1, Depth, PlayerB, Get_Position(i, j))

	                this_move_type = Get_Move_Type(state, i, j, player)

	                if (cur_val == v and cur_type == "Raid"):
	                	if this_move_type == "Stake":
	                		cur_type = "Stake"
	                		cur_position = [Get_Position(i, j), i, j, cur_type]	

	                if (cur_val > v):
	                    v = cur_val
	                    cur_type = this_move_type
	                    cur_position = [Get_Position(i, j), i, j, cur_type]
	                

	                v = max(v, cur_val)

	                if (v > beta):
	                	return v
	                alpha = max(alpha, v)

        if (position == "start"):
			return cur_position
        return v
    else:
        v = float('inf')
        for i in range(0, N):
            for j in range(0, N):
                if state[i][j] == ".":
	                new_board = Get_Next_State(state, i, j, player)
	                cur_val = Alpha_Beta_Search(new_board, alpha, beta, cur_depth + 1, Depth, PlayerA, Get_Position(i, j))
	                v = min(v, cur_val)
	                if (v < alpha):
	                	return v
	                beta = min(beta, v)
        return v

result = []

if(Mode == "MINIMAX"):
	result = Minimax_Search(cur_board, 0, Depth, PlayerA, "start")
if(Mode == "ALPHABETA"):
	result = Alpha_Beta_Search(cur_board, float('-inf'), float('inf'), 0, Depth, PlayerA, "start")

# result = Alpha_Beta_Search(cur_board, float('-inf'), float('inf'), 0, Depth, PlayerA, "start")
# result = Minimax_Search(cur_board, 0, Depth, PlayerA, "start")

# print result
final_move = result[0]
# final_move_type = Get_Move_Type(cur_board, result[1], result[2], PlayerA)
final_move_type = result[3]
# final_board = Get_Next_State(cur_board, result[1], result[2], PlayerA)
final_board = Get_Final_board(cur_board, result[1], result[2], PlayerA, final_move_type)

# print final_move + " " + final_move_type

# for i in range(0, N):
#     row = ""
#     for j in range(0, N):
#         row += final_board[i][j]
#     print row

fout = open("output.txt", "w+")
fout.write(final_move + " " + final_move_type + '\n')
for i in range(0, N):
    row = ""
    for j in range(0, N):
        row += final_board[i][j]
    fout.write(row)
    if(i == N-1):
        exit()
    fout.write('\n')
