import random



def generate_random_maze(width, height):
    maze = [['1' for _ in range(width)] for _ in range(height)]

    def carve_maze(x, y):
        maze[y][x] = '0'

        directions = [(x-2, y), (x, y+2), (x+2, y), (x, y-2)]
        random.shuffle(directions)

        for dx, dy in directions:
            if 0 <= dx < width and 0 <= dy < height and maze[dy][dx] == '1':
                maze[(y + dy) // 2][(x + dx) // 2] = '0'
                carve_maze(dx, dy)

    carve_maze(1, 1)

    # Add border walls
    for i in range(width):
        maze[0][i] = '1'
        maze[height - 1][i] = '1'
    for i in range(height):
        maze[i][0] = '1'
        maze[i][width - 1] = '1'

    with open('RandomMaze', 'w') as f:
        for row in maze:
            f.write(''.join(row))
            f.write('\n')


def generate_alt_maze(width, height):
    maze = [['1' for _ in range(width)] for _ in range(height)]

    def carve_maze(x, y):
        maze[y][x] = '_'

        directions = [(x-2, y), (x, y+2), (x+2, y), (x, y-2)]
        random.shuffle(directions)

        for dx, dy in directions:
            if 0 <= dx < width and 0 <= dy < height and maze[dy][dx] == '1':
                maze[(y + dy) // 2][(x + dx) // 2] = '_'
                carve_maze(dx, dy)

    # Carve main maze
    carve_maze(1, 1)

    # Create breakable blocks
    num_blocks = random.randint(2, 4)
    for _ in range(num_blocks):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        maze[y][x] = '2'

    # Add border walls
    for i in range(width):
        maze[0][i] = '1'
        maze[height - 1][i] = '1'
    for i in range(height):
        maze[i][0] = '1'
        maze[i][width - 1] = '1'

    with open('RandomMaze', 'w') as f:
        for row in maze:
            f.write(','.join(row))
            f.write('\n')
