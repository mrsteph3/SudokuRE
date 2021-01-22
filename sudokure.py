import random
import sys
import pygame

# Number of game ticks per second
GAME_FPS = 15

# Dimensions
WINDOW_MULT = 10 # Change the scale of the window HERE.
WINDOW_SIZE = 81 # Must be size N, where N % 81 == 0.
WINDOW_WIDTH = WINDOW_SIZE * WINDOW_MULT
WINDOW_HEIGHT = WINDOW_SIZE * WINDOW_MULT
WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
SQUARE_SIZE = (WINDOW_SIZE * WINDOW_MULT) // 3
CELL_SIZE = SQUARE_SIZE // 3
NUMBER_SIZE = CELL_SIZE // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREY  = (200, 200, 200)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)

# Difficulty Level
DIFFICULTY = 5 # a number from [1, 9] where lower is easier.

# Function used for testing purposes and does not print to the game window.
def printBoard(b):
    '''
    Prints a game board to the command line.

            Parameters:
                    b (list(list(int))): A list of lists containing integers.

            Returns:
                    None
    '''
    for i in range(len(b)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')
        for j in range(len(b)):
            if j % 3 == 0 and j != 0:
                print(' | ', end='')
            if j == 8:
                print(b[i][j])
            else:
                print(str(b[i][j]) + '', end=' ')


def validate(b, row, col, n) -> bool:
    '''
    Returns whether an integer, n, can be placed at b[row][col] without conflict.

            Parameters:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.
                    row           (int): An integer representing the row of the cell.
                    col           (int): An integer representing the column of the cell.
                    n             (int): An integer representing the number
                                            to be added to the board.

            Returns:
                    (bool): A boolean value
    '''
    for i in range(9):
        # Check the row for n, not including the current space
        if b[row][i] == n and col != i:
            return False
        # Check the col for n, not including the current space
        if b[i][col] == n and row != i:
            return False

    # Get the 3x3 box that the row and column are referring to
    boxX = col // 3
    boxY = row // 3

    # Check the 3x3 box for n, not including the current space
    for i in range(boxY * 3, boxY * 3 + 3):
        for j in range(boxX * 3, boxX *3 + 3):
            if b[i][j] == n and not (i == row and j == col):
                return False
    return True


def solve(b, row, col) -> bool:
    '''
    Returns True the board can be solved, else False.

            Parameters:
                    b   (list(list(int))): A list of lists containing integers.
                    row             (int): An integer representing the row of the cell.
                    col             (int): An integer representing the column of the cell.

            Returns:
                    (bool): A boolean value
    '''
    last = False

    # If the column number exceeds the number of columns in the board,
    # Reset the column number to 0 and increment the row number by 1.
    if col == 9:
        row += 1
        col = 0

    # If we are checking the last cell of the board, set the last variable to True
    # so that we can exit the function properly.
    if row == 8 and col == 8:
        last = True

    # For all empty cells, try numbers in the interval [1,9] and:
    # if the number is valid, recurse to the next cell and repeat the process.
    # if the number is invalid check the next number in the interval.
    # if all numbers have been exhausted with no solution, return False.
    if b[row][col] == 0:
        for i in range(1,10):
            if validate(b, row, col, i):
                b[row][col] = i
                if last:
                    return True
                else:
                    if solve(b, row, col+1):
                        return True
        b[row][col] = 0

    # If the cell is not empty, check if the current cell is the last.
    # If the current cell is the last, return True
    # Else, continue to the next cell.
    else:
        if last:
            return True
        else:
            if solve(b, row, col+1):
                return True
    return False


def generateBoard():
    '''
    Generates a completed game board with randomized numbers

            Parameters:
                    None

            Returns:
                    (list(list(int))): A 2D integer list representing a
                                         completed sudoku game board.
    '''
    board = []
    firstLine = []

    # Fill the first row with random integers in the interval [1,9]
    while len(firstLine) < 9:
        num = random.randint(1, 9)
        if num not in firstLine:
            firstLine.append(num)

    # Add the first row to the board
    board.append(firstLine)

    # For each subsequent row, if the row number is divisble by 3,
    # Rotate the previous row by 1 index.
    # Else, rotate the previous row by 3 indices.
    for i in range(1,9):
        line = []
        if i % 3 != 0:
            line = board[i-1][3:] + board[i-1][:3]
        else:
            line = board[i-1][1:] + board[i-1][:1]
        board.append(line)
    return board


def removeRandom(b):
    '''
    Removes a random cell from the game board.

            Parameters:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.

            Returns:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.
    '''
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    temp = b[row][col]
    b[row][col] = 0
    copy = []
    for line in b:
        lineTemp = []
        for num in line:
            lineTemp.append(num)
        copy.append(lineTemp)
    if solve(copy, 0, 0):
        return b
    else:
        b[row][col] = temp
        return b


def canComplete(b, row, col, n):
    '''
    Returns True if the game board, b, can be completed without actually completing the game board.

            Parameters:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.
                    row           (int): An integer representing the row of the cell.
                    col           (int): An integer representing the column of the cell.
                    n             (int): An integer representing the number
                                            to be added to the board.

            Returns:
                    (bool): A boolean value
    '''

    # Make a copy of the board so that the real board is not changed by solve().
    copy = []
    for line in b:
        lineTemp = []
        for num in line:
            lineTemp.append(num)
        copy.append(lineTemp)

    # Check if the copy can be solved from that point.
    copy[row][col] = n
    if solve(copy, 0, 0):
        return True
    else:
        return False


def numHints(b) -> int:
    '''
    Returns the number of non-zero cells in the game board, b.

            Parameters:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.

            Returns:
                    res           (int): An integer.
    '''

    # Simple 2D list traversal with a counter variable.
    res = 0

    for col in range(9):
        for row in range(9):
            if b[row][col] != 0:
                res += 1

    return res


def getSelectedCell(mouseX, mouseY):
    '''
    Returns a 3-tuple containing the row, column, and Rectangle object from the mouse position.

            Parameters:
                    mouseX        (int): An integer representing the x-coordinate of the cursor.
                    mouseY        (int): An integer representing the y-coordinate of the cursor.

            Returns:
                    ((int, int, Rect): A 3-tuple containing the row, column, and Rectangle object.
    '''
    numX = (mouseX * 27) // WINDOW_WIDTH
    numY = (mouseY * 27) // WINDOW_HEIGHT
    col = numX // 3
    row = numY // 3

    selectionRect = pygame.rect.Rect((col)*CELL_SIZE, (row)*CELL_SIZE, CELL_SIZE, CELL_SIZE)

    return (row, col, selectionRect)


def displayCells(b):
    '''
    Iterates through the cells in b and sends the information to populateCells() to draw.

            Parameters:
                    b (list(list(int))): A 2D integer list representing a
                                            completed sudoku game board.

            Returns:
                    None
    '''
    for row in range(len(b)):
        for col in range(len(b[row])):
            if b[row][col] != 0:
                num = b[row][col]
                x_location = col*CELL_SIZE + (2 * WINDOW_MULT)
                y_location = row*CELL_SIZE + (0.5 * WINDOW_MULT) // 1
                populateCell(num, x_location, y_location)


def populateCell(number, x, y):
    '''
    Displays the number at the x, y coordinates on the screen.

            Parameters:
                    number (int): An integer representing the number for draw on the screen.
                    x      (int): An integer representing the x-coordinate to draw at.
                    y      (int): An integer representing the y-coordinate to draw at.

            Returns:
                    None
    '''
    cellSurface = FONT.render('%s' %(number), True, BLACK)
    cellRectangle = cellSurface.get_rect()
    cellRectangle.topleft = (x, y)
    DISPLAY.blit(cellSurface, cellRectangle)


def drawLines():
    '''
    Draws the lines to separate the cells on the game window.

            Parameters:
                    None

            Returns:
                    None
    '''

    # Grey lines to distinguish 9x9 Cells
    for i in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAY, GREY, (i, 0), (i, WINDOW_HEIGHT))
    for i in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAY, GREY, (0, i), (WINDOW_WIDTH, i))

    # Black lines to distinguish 3x3 Squares
    for i in range(0, WINDOW_WIDTH, SQUARE_SIZE):
        pygame.draw.line(DISPLAY, BLACK, (i, 0), (i, WINDOW_HEIGHT))
    for i in range(0, WINDOW_HEIGHT, SQUARE_SIZE):
        pygame.draw.line(DISPLAY, BLACK, (0, i), (WINDOW_WIDTH, i))


def main():
    '''
    Main function which initializes pygame and holds the main game loop.

            Parameters:
                    None

            Returns:
                    None
    '''
    # Initialize pygame and window
    pygame.init()
    pygame.display.set_caption('SudokuRE')

    # DISPLAY AND CLOCK initialization
    global DISPLAY, CLOCK
    DISPLAY = pygame.display.set_mode(WINDOW_DIMENSIONS)
    CLOCK = pygame.time.Clock()

    # FONT and FONTSIZE initialization
    global FONT, FONTSIZE
    FONTSIZE = WINDOW_MULT * 9
    FONT = pygame.font.SysFont('Arial', FONTSIZE)

    # Generate the puzzle based on the DIFFICULTY
    board = generateBoard()
    while numHints(board) > 15 + ((10-DIFFICULTY)*5):
        board = removeRandom(board)
    printBoard(board)

    # Prepare the board for first viewing
    DISPLAY.fill(WHITE)
    drawLines()
    displayCells(board)

    # Mouse and selection variables
    global SELECTION
    mouseClicked = False
    selectionMade = False
    mouseX = mouseY = 0
    selectionRow = selectionCol = 0

    # Main game loop
    while True:

        mouseClicked = False

        for event in pygame.event.get():

            # If the window is closed, quit the game and close the process.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user clicks, get the x and y coords and set mouseClicked to True.
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

            # If the user presses a key check the key.
            elif event.type == pygame.KEYDOWN:

                # If the key is from 1-9, check to see if the user has selected a cell.
                if event.key == pygame.K_1:

                    if selectionMade:

                        # If the user can complete the game by making this selection,
                        # allow them to insert it.
                        if canComplete(board, selectionRow, selectionCol, 1):
                            board[selectionRow][selectionCol] = 1
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 1, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_2:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 2):
                            board[selectionRow][selectionCol] = 2
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 2, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_3:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 3):
                            board[selectionRow][selectionCol] = 3
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 3, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_4:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 4):
                            board[selectionRow][selectionCol] = 4
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 4, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_5:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 5):
                            board[selectionRow][selectionCol] = 5
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 5, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_6:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 6):
                            board[selectionRow][selectionCol] = 6
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 6, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_7:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 7):
                            board[selectionRow][selectionCol] = 7
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 7, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_8:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 8):
                            board[selectionRow][selectionCol] = 8
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 8, 'at', selectionRow, selectionCol)

                elif event.key == pygame.K_9:
                    if selectionMade:

                        if canComplete(board, selectionRow, selectionCol, 9):
                            board[selectionRow][selectionCol] = 9
                            DISPLAY.fill(WHITE)
                            displayCells(board)
                            drawLines()

                        else:
                            print('Cannot insert', 9, 'at', selectionRow, selectionCol)

                # If the key is SPACE, try to solve the puzzle.
                elif event.key == pygame.K_SPACE:
                    if not solve(board, 0, 0):
                        print('Board can not be solved!')


        # If the mouse was clicked, set the rect, selectionRow, and selectionCol variables
        if mouseClicked:
            selectionRow, selectionCol, rect = getSelectedCell(mouseX, mouseY)
            selectionMade = True
            SELECTION = rect

        # Refresh board
        DISPLAY.fill(WHITE)
        displayCells(board)
        drawLines()

        # If the game has been solved, color the board GREEN and wait 10 seconds before exiting
        if numHints(board) == 81:
            DISPLAY.fill(GREEN)
            displayCells(board)
            drawLines()

        # Draw the RED box around the cell that is selected
        if selectionMade:
            pygame.draw.rect(DISPLAY, RED, SELECTION, 2)

        # Update the display and tick the game CLOCK
        pygame.display.update()
        CLOCK.tick(GAME_FPS)


if __name__ == '__main__':
    main()
