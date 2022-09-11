import random
import time
import tkinter

def print_board(board):
    for row in board:
        print(row)

def get_frontier_tiles(board, owned_tiles):
    frontier_tiles = []
    for tile in owned_tiles:
        if tile[0]-1 >= 0 and (tile[0]-1, tile[1]) not in owned_tiles:
            frontier_tiles.append((tile[0]-1, tile[1]))
        if tile[0]+1 < len(board) and (tile[0]+1, tile[1]) not in owned_tiles:
            frontier_tiles.append((tile[0]+1, tile[1]))
        if tile[1]-1 >= 0 and (tile[0], tile[1]-1) not in owned_tiles:
            frontier_tiles.append((tile[0], tile[1]-1))
        if tile[1]+1 < len(board[0])  and (tile[0], tile[1]+1) not in owned_tiles:
            frontier_tiles.append((tile[0], tile[1]+1))
    return frontier_tiles

def calculate_move(board, frontier_tiles):
    color_puntuation = [0 for i in range(len(colors))]
    for tile in frontier_tiles:
        color_puntuation[board[tile[0]][tile[1]]] += eval_tile(board, tile)
    print(color_puntuation)
    return color_puntuation.index(max(color_puntuation))

def eval_tile(board, tile, explored_tiles=None):
    tile_color = board[tile[0]][tile[1]]
    puntuation = 0
    if explored_tiles is None:
        explored_tiles = []
        puntuation += 1
    explored_tiles.append(tile)
    if tile[0]-1 >= 0:
        if board[tile[0]-1][tile[1]] == tile_color and (tile[0]-1, tile[1]) not in explored_tiles:
            puntuation += 1
            puntuation += eval_tile(board, (tile[0]-1, tile[1]), explored_tiles) 
    if tile[0]+1 < len(board):
        if board[tile[0]+1][tile[1]] == tile_color and (tile[0]+1, tile[1]) not in explored_tiles:
            puntuation += 1
            puntuation += eval_tile(board, (tile[0]+1, tile[1]), explored_tiles)
    if tile[1]-1 >= 0:
        if board[tile[0]][tile[1]-1] == tile_color and (tile[0], tile[1]-1) not in explored_tiles:
            puntuation += 1
            puntuation += eval_tile(board, (tile[0], tile[1]-1), explored_tiles)
    if tile[1]+1 < len(board[0]):
        if board[tile[0]][tile[1]+1] == tile_color and (tile[0], tile[1]+1) not in explored_tiles:
            puntuation += 1
            puntuation += eval_tile(board, (tile[0], tile[1]+1), explored_tiles)
    return puntuation

def color_tiles(board, owned_tiles, color):
    print("Coloring tiles with color: {}".format(colors[color]))
    for tile in owned_tiles:
        board[tile[0]][tile[1]] = color

def append_new_tiles(board, owned_tiles, color):
    new_tiles = []
    for tile in owned_tiles:
        if tile[0]-1 >= 0 and (tile[0]-1, tile[1]) not in owned_tiles:
            if board[tile[0]-1][tile[1]] == color:
                owned_tiles.append((tile[0]-1, tile[1]))
                new_tiles.append((tile[0]-1, tile[1]))
        if tile[0]+1 < len(board) and (tile[0]+1, tile[1]) not in owned_tiles:
            if board[tile[0]+1][tile[1]] == color:
                owned_tiles.append((tile[0]+1, tile[1]))
                new_tiles.append((tile[0]+1, tile[1]))
        if tile[1]-1 >= 0 and (tile[0], tile[1]-1) not in owned_tiles:
            if board[tile[0]][tile[1]-1] == color:
                owned_tiles.append((tile[0], tile[1]-1))
                new_tiles.append((tile[0], tile[1]-1))
        if tile[1]+1 < len(board[0])  and (tile[0], tile[1]+1) not in owned_tiles:
            if board[tile[0]][tile[1]+1] == color:
                owned_tiles.append((tile[0], tile[1]+1))
                new_tiles.append((tile[0], tile[1]+1))
    return new_tiles

def calculate():
    # get time
    init_time = time.time()
    frontier_tiles = get_frontier_tiles(board, owned_tiles)
    # remove repeated tiles
    frontier_tiles = list(set(frontier_tiles))
    selected_color = calculate_move(board, frontier_tiles)
    print("Selected color: {}".format(colors[selected_color]))
    color_tiles(board, owned_tiles, selected_color)
    for tile in frontier_tiles:
        if board[tile[0]][tile[1]] == selected_color:
            owned_tiles.append(tile)
    # print_board(board)
    new_tiles = append_new_tiles(board, owned_tiles, selected_color)
    if len(owned_tiles) == board_size * board_size:
        print("Game over")
        root.quit()
    finish_time = time.time()
    print("Time calcultating: {}".format(finish_time - init_time))
    init_time = time.time()
    update_canvas()
    finish_time = time.time()
    print("Time updating canvas: {}".format(finish_time - init_time))

def update_canvas():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, rectangle_size * board_size, rectangle_size * board_size, fill=colors[board[0][0]], width=0)
    for i in range(board_size):
        for j in range(board_size):
            if (i, j) not in owned_tiles:
                canvas.create_rectangle(i * rectangle_size, j * rectangle_size, i * rectangle_size + rectangle_size, j * rectangle_size + rectangle_size, fill=colors[board[i][j]], width=0)
    canvas.update()
    # check if game is over
    root.after(speed, calculate)

while True:
    # THEMES:
    # Basic
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    # # Rainbow
    # colors = ['#BD1354', '#E46C21', '#E2A61D', '#2EA32C', '#3653EE', '#572083']
    # # Vintage
    colors = ['#3F3B33', '#92504C', '#DA9F5F', '#E6C89D', '#748A5E', '#32415E']
    owned_tiles = [(0,0)]
    frontier_tiles = owned_tiles

    speed = 250
    n_colors = 6
    board_size = 100
    rectangle_size = 10
    board = [[random.randint(0, n_colors - 1) for _ in range(board_size)] for _ in range(board_size)]
    print_board(board)
    append_new_tiles(board, owned_tiles, board[0][0])

    root = tkinter.Tk()
    root.title("Board")
    canvas = tkinter.Canvas(root, width=board_size * rectangle_size, height=board_size * rectangle_size)
    canvas.pack()
    for i in range(board_size):
        for j in range(board_size):
            canvas.create_rectangle(i * rectangle_size, j * rectangle_size, i * rectangle_size + rectangle_size, j * rectangle_size + rectangle_size, fill=colors[board[i][j]], width=0)
    button = tkinter.Button(root, text="Continue", command=update_canvas)
    button.pack()
    button = tkinter.Button(root, text="Calculate", command=calculate)
    button.pack()
    root.after(speed, calculate)
    root.mainloop()
    root.destroy()