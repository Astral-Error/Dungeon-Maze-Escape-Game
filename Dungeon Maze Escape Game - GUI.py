import pygame
import random
import pyautogui as pgi

#This function displays the entire maze
def display_maze():
    for row in maze:
        print(" ".join(row))

#Returns the current position of the player in the maze
def position(character):
    for row in range(len(maze)):
        if character in maze[row]:
            return [row,maze[row].index(character)]

#Updates the player position in the map depending on the user input
def player_movement(move):
    row,column = position("P")
    if move=="up":
        row_n = move_up(row,column)
        update_maze(row,column,row_n,column)

    if move=="down":
        row_n = move_down(row,column)
        update_maze(row,column,row_n,column)

    if move=="left":
        column_n = move_left(row,column)
        update_maze(row,column,row,column_n)

    if move=="right":
        column_n = move_right(row,column)
        update_maze(row,column,row,column_n)

#Adjusts player position for upward movement
def move_up(row,column):
    if row!=0:
        if maze[row-1][column]!="#":
            return row-1
        else: 
            print("\nCan't move up!!\n")
            return row
    else:
        print("\nCant move up!!\n")
        return row

#Adjusts player position for downward movement
def move_down(row,column):
    if row!=len(maze)-1:
        if maze[row+1][column]!="#":
            return row+1
        else: 
            print("\nCan't move down!!\n")
            return row
    else:print("\nCant move down!!\n")

#Adjusts player position for left movement
def move_left(row,column):
    if column!=0:
        if maze[row][column-1]!="#":
            return column-1
        else: 
            print("\nCan't move left!!\n")
            return column
    else:print("\nCant move left!!\n")


#Adjusts player position for right movement
def move_right(row,column):
    if column!=len(maze[0])-1:
        if maze[row][column+1]!="#":
            return column+1
        else: 
            print("\nCan't move right!!\n")
            return column
    else:print("\nCant move right!!\n")

#Updates the current player position WRT movement
def update_maze(row,column,row_n,column_n):
    if [row,column]!=[row_n,column_n]:
        maze[row][column]=" "
        maze[row_n][column_n]="P"
    else:
        return False

#This function procedurally generates a maze with a single path to the exit
def maze_generation():
    #Generates the random values for the maze
    global row_col
    row_col = random.randint(random.randint(50,60),random.randint(60,70))
    global entry_column
    entry_column = random.randint(1,row_col-3) #A gap of two is left to avoid conflict with column ends
    exit_column = random.randint(0,row_col-1) 

    #Maze creation
    maze=[]
    for i in range(row_col):
        maze+=[[]] #Creates the respective rows
        for j in range(row_col):
            maze[i]+=["#"] #Creates the respective columns

    #The following snippet creates the entry point of the maze
    maze[0][entry_column]="P"
    origin_row,origin_column = 0,entry_column
    flag_columEnd = flag_columnBegin = False

    #The following loop generates the pathway to the end for the user to navigate.
    while origin_row!=len(maze)-1:
        #The block uses the columnEnd Flag to determine whether the path generator is at the right end of the maze
        if origin_column==len(maze[0])-2:
            flag_columEnd = True
        
        #This block checks whether the path gen from the right end has reached the left column end of the maze
        if flag_columEnd and origin_column==1:
            flag_columnBegin = True
        
        randomizer=random.randint(1,2000)
        if randomizer%2==0: #If randomizer value is even the gap is made in a row
            if origin_row+1<len(maze):
                maze[origin_row+1][origin_column]=" "
                origin_row+=1
            else:
                maze[origin_row][origin_column]=" "
        else: #For an odd randomizer value the gap is created in the column
            if not flag_columEnd or flag_columnBegin: #When the path gen is at the left most side
                maze[origin_row][origin_column+1]=" "
                origin_column+=1
            elif flag_columEnd: #When the path gen is at the right most side
                maze[origin_row][origin_column-1]=" "
                origin_column-=1

    return maze

#This function configures the maze with random spaces throughtout to create false paths
def maze_config():
    row,column=len(maze),len(maze[0])
    for i in range(1,row-1):
        #Randomly generates the number of blanks to add in each row
        no_of_blanks = random.randint(row-row//5,column-2)
        for j in range(no_of_blanks):
            maze[i][random.randint(1,column-2)]=" "
    return maze

def draw_maze():
    for row in range(grid_height):
        for col in range(grid_width):
            cell = maze[row][col]
            color = white

            if cell=="#": color = wall_color
            elif [row, col] == position("P"):
                color=player_color
            elif [row, col]==exit_pos:
                color = exit_color

            pygame.draw.rect(
                screen, color,
                pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
            )


maze = maze_generation() #Generates the maze with the path
exit_pos = [len(maze)-1,maze[len(maze)-1].index(" ")]
maze = maze_config() #Configures the entire maze with random pathways
#display_maze()
flag_firstMove = True
    
cell_size = 13
grid_width, grid_height = row_col,row_col
screen_width, screen_height = grid_width * cell_size, grid_height*cell_size

white = (223, 223, 223)
black = (33, 39, 23)
player_color = (41,128,185)
enemy_color = (255, 0, 0)
exit_color = (247, 202, 121)
wall_color = (56, 56, 56)
player_pos = position("P")

#Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dungeon Maze Escape")
clock = pygame.time.Clock()

pgi.alert("• The blue mark in the top row indicates the player position\n\
• The yellow mark at the bottom most row indicates the exit\n\
• The black marks represents walls or barriers\n\
• Use arrow keys for movement".center(10))

quit_flag=True
running = True
while running and exit_pos!=position("P"):
    screen.fill(white)
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_flag = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_movement("up")
            elif event.key == pygame.K_DOWN:
                player_movement("down")
            elif event.key == pygame.K_LEFT:
                player_movement("left")
            elif event.key == pygame.K_RIGHT:
                player_movement("right")
        
    draw_maze()
    pygame.display.flip()
    clock.tick(60)
if quit_flag: pgi.alert("Congratulations!!, you finished the game")
pygame.quit()