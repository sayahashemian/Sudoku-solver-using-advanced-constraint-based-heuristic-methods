import time
import math

def find_empty_location(arr, l):
    """
    Finds the next empty location (represented by 0) in the Sudoku grid
    """
    subgrid = int(math.sqrt(len(arr)))
    min_values = float('inf')
    for row in range(len(arr)):
        for col in range(len(arr)):
            if arr[row][col] == 0:
                values = set(range(1, len(arr)+1)) - set(arr[row]) - set(arr[i][col] for i in range(len(arr))) - set(arr[row//subgrid*subgrid+i][col//subgrid*subgrid+j] for i in range(subgrid) for j in range(subgrid))
                if len(values) < min_values:
                    l[0] = row
                    l[1] = col
                    min_values = len(values)
    return min_values != float('inf')

def used_in_row(arr, row, num):
    """
    Checks if a given number is already present in a row
    """
    for i in range(len(arr)):
        if arr[row][i] == num:
            return True
    return False


def used_in_col(arr, col, num):
    """
    Checks if a given number is already present in a column
    """
    for i in range(len(arr)):
        if arr[i][col] == num:
            return True
    return False


def used_in_box(arr, row, col, num):
    """
    Checks if a given number is already present in the 3x3 box
    """
    subgrid = int(math.sqrt(len(arr)))
    for i in range(subgrid):
        for j in range(subgrid):
            if arr[i + row][j + col] == num:
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    """
    Checks if it is safe to assign a given number to a particular location
    """
    subgrid = int(math.sqrt(len(arr)))
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % subgrid, col - col % subgrid, num)


def solve_sudoku(arr):
    """
    Solves the Sudoku grid using backtracking with MRV, LCV, and forward checking heuristics
    """
    l = [0, 0]
    subgrid = int(math.sqrt(len(arr)))
    if not find_empty_location(arr, l):
        return True

    row = l[0]
    col = l[1]

    values = set(range(1, len(arr)+1)) - set(arr[row]) - set(arr[i][col] for i in range(len(arr))) - set(arr[row//subgrid*subgrid+i][col//subgrid*subgrid+j] for i in range(subgrid) for j in range(subgrid))
    values = sorted(values, key=lambda x: sum(1 for i in range(len(arr)) for j in range(subgrid) for k in range(subgrid) if arr[row][i] == x or arr[i][col] == x or arr[row//subgrid*subgrid+j][col//subgrid*subgrid+k] == x))

    for num in values:
        if check_location_is_safe(arr, row, col, num):
            arr[row][col] = num

            # Forward checking
            constraints = []
            for i in range(len(arr)):
                if arr[row][i] == 0 and not check_location_is_safe(arr, row, i, num):
                    constraints.append((row, i))
                if arr[i][col] == 0 and not check_location_is_safe(arr, i, col, num):
                    constraints.append((i, col))
                box_row = subgrid * (row // subgrid) + i // subgrid
                box_col = subgrid * (col // subgrid) + i % subgrid
                if arr[box_row][box_col] == 0 and not check_location_is_safe(arr, box_row, box_col, num):
                    constraints.append((box_row, box_col))
            if forward_check(arr, constraints):
                if solve_sudoku(arr):
                    return True

            arr[row][col] = 0

    return False


def forward_check(arr, constraints):
    """
    Propagates the constraints of the current assignment to the remaining empty locations
    """
    subgrid = int(math.sqrt(len(arr)))

    for row, col in constraints:
        values = set(range(1, len(arr)+1)) - set(arr[row]) - set(arr[i][col] for i in range(len(arr))) - set(arr[row//subgrid*subgrid+i][col//subgrid*subgrid+j] for i in range(subgrid) for j in range(subgrid))
        if not values:
            return False
    return True


def printSudoku(arr):
    subgrid = int(math.sqrt(len(arr)))

    for i in range(len(arr)):
        if i % subgrid == 0 and i != 0:
            print(".....................")

        for j in range(len(arr[0])):
            if j % subgrid == 0 and j != 0:
                print("|", end=" ")

            if j == len(arr[0])-1:
                print(arr[i][j])
            else:
                print(str(arr[i][j]) + " ", end="")

n = int(input("please enter n: "))
c = int(input("please enter c: "))

board = [[0] * n for i in range(n)]
# board = [
#          [0, 6, 0, 0, 0, 0, 0, 8, 11, 0, 0, 15, 14, 0, 0, 16],
#          [15, 11, 0, 0, 0, 16, 14, 0, 0, 0, 12, 0, 0, 6, 0, 0],
#          [13, 0, 9, 12, 0, 0, 0, 0, 3, 16, 14, 0, 15, 11, 10, 0],
#          [2, 0, 16, 0, 11, 0, 15, 10, 1, 0, 0, 0, 0, 0, 0, 0],
#          [0, 15, 11, 10, 0, 0, 16, 2, 13, 8, 9, 12, 0 ,0 ,0 ,0],
#          [12, 13, 0, 0, 4, 1, 5, 6, 2, 3, 0, 0, 0, 0, 11, 10],
#          [5, 0, 6, 1, 12, 0, 9, 0, 15, 11, 10, 7, 16, 0, 0, 3],
#          [0, 2, 0, 0, 0, 10, 0, 11, 6, 0, 5, 0, 0, 13, 0, 9],
#          [10, 7, 15, 11, 16, 0, 0, 0, 12, 13, 0, 0, 0, 0, 0, 6],
#          [9, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 16, 10, 0, 0, 11],
#          [1, 0, 4, 6, 9, 13, 0, 0, 7, 0, 11, 0, 3, 16, 0, 0],
#          [16, 14, 0, 0, 7, 0, 10, 15, 4, 6, 1, 0, 0, 0, 13, 8],
#          [11, 10, 0, 15, 0, 0, 0, 16, 9, 12, 13, 0, 0, 1 ,5 ,4],
#          [0, 0, 12, 0, 1, 4, 6, 0, 16, 0, 0, 0, 11, 10, 0, 0],
#          [0, 0, 5, 0, 8, 12, 13, 0, 10, 0, 0, 11, 2, 0, 0, 14],
#          [3, 16, 0, 0, 10, 0, 0, 7, 0, 0, 6, 0, 0, 0, 12, 0],
#     ]

for k in range(c):
    i, j, value = map(int, input("Enter (i, j, value): ").split())
    board[i][j] = value

printSudoku(board)
print("============================================================")
start_time = time.time()
check = solve_sudoku(board)

if check == False:
    print("Unsolvable CSP!")
else:
    printSudoku(board)

end_time = time.time()

print(end_time - start_time)




