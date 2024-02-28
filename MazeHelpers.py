import pathlib
import random
import numpy as np
from matplotlib import colors
from matplotlib import animation, rc
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib import colors
rc('animation', html='html5')

def parse_maze(maze_str):
    """Convert a maze as a string into a 2d numpy array"""
    maze = maze_str.split('\n')
    maze = np.array([[tile for tile in row] for row in maze if len(row) > 0])
        
    return maze

# show_maze: Code by Nicholas Crothers modified and expanded by M. Hahsler
# This is modified code I found on StackOverflow, at this link
# https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values
def show_maze(maze, fontsize = 10):  
    """Display a (parsed) maze as an image."""
   
    cmap = colors.ListedColormap(['white', 'black', 'blue', 'green', 'red', 'gray', 'orange'])
    
    # make a deep copy first so the original maze is not changed. Python passes objects by reference!
    maze = np.copy(maze)
    
    goal = find_pos(maze, 'G')
    start = find_pos(maze, 'S')
    
    # Converts all tile types to integers
    maze[maze == ' '] = 0
    maze[maze == 'X'] = 1 # wall
    maze[maze == 'S'] = 2 # start
    maze[maze == 'G'] = 3 # goal
    maze[maze == 'P'] = 4 # position/final path
    maze[maze == '.'] = 5 # explored squares
    maze[maze == 'F'] = 6 # frontier
    maze = maze.astype(int)
    
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap = cmap, norm = colors.BoundaryNorm(list(range(cmap.N + 1)), cmap.N))
    
    plt.text(start[1], start[0], "S", fontsize = fontsize, color = "white",
                 horizontalalignment = 'center',
                 verticalalignment = 'center')
    
    plt.text(goal[1], goal[0], "G", fontsize = fontsize, color = "white",
                 horizontalalignment = 'center',
                 verticalalignment = 'center')
    
    plt.show()
    
def find_pos(maze, what = "S"):
    """
    Find start/goal in a maze and returns the first one. 
    Caution: there is no error checking!
    
    Parameters:
    maze: a array with characters prodced by parse_maze()
    what: the letter to be found ('S' for start and 'G' for goal)
    
    Returns:
    a tupple (x, y) for the found position.
    """
    
    # where returns two arrays with all found positions. We are only interested in the first one at index 0.
    pos = np.where(maze == what)
    return(tuple([pos[0][0], pos[1][0]]))

def look(maze, pos):
    """Look at the label of a square with the position as an array of the form (x, y)."""
    
    x, y = pos
    return(maze[x, y])



def welcome():
    """Welcome message."""
    
    print("""Helper functions for the Maze Assignment by M. Hahsler
Usage: 
  import maze_helper as mh
  mh.show_some_mazes()
  
Here is an example maze:
""")

    with open(f"small_maze.txt", "r") as f:    
        maze_str = f.read()
        print(maze_str)
            
        maze = parse_maze(maze_str)
        goal = find_pos(maze, what = "G")
        print(f"The goal is at {goal}.")
    
def maze_to_matrix(maze):  
        """convert a maze a numeric numpy array for visualization via imshow."""

        # make a deep copy first so the original maze is not changed
        maze = np.copy(maze)
        
        # Converts all tile types to integers
        maze[maze == ' '] = 0
        maze[maze == 'X'] = 1 # wall
        maze[maze == 'S'] = 2 # start
        maze[maze == 'G'] = 3 # goal
        maze[maze == 'P'] = 4 # position/final path
        maze[maze == '.'] = 5 # explored squares
        maze[maze == 'F'] = 6 # frontier
        maze = maze.astype(int)
        
        return(maze)

def paint_path(path,maze,value):
    """path: List of tuples describing the x, y coordinates of the node
    maze: The maze as a 2d numpy array
    value: character to put in the path
    Usage: paint_path([(0,0),(1,0),(2,0),(1,1)],np.array(shape=(0,0)),value='F')
    """

    for val in path:
        if maze[val[1]][val[0]] != 'S' and maze[val[1]][val[0]] != 'G':
            maze[val[1]][val[0]] = value

def animate_maze(mazes, fileName=None,repeat = False,goal_show_frames=5):
            """Build an animation from a list of mazes. Assumes that results has the elements:
            path, reached, actions and maze_anim with a list of maze arrays."""
            _mazes = mazes.copy()
            for _ in range(goal_show_frames):
                 _mazes.append(mazes[-1])
            
            
            cmap = colors.ListedColormap(['white', 'black', 'blue', 'green', 'red', 'gray', 'orange'])
    
            goal = find_pos(_mazes[0], 'G')
            start = find_pos(_mazes[0], 'S')
    
            _mazes = [maze_to_matrix(m) for m in _mazes]

            fig, ax = plt.subplots()
            im = ax.imshow(maze_to_matrix(_mazes[0]), cmap = cmap, norm = colors.BoundaryNorm(list(range(cmap.N + 1)), cmap.N))
    
            plt.text(start[1], start[0], "S", fontsize = 10, color = "white",
                    horizontalalignment = 'center',
                    verticalalignment = 'center')
    
            plt.text(goal[1], goal[0], "G", fontsize = 10, color = "white",
                    horizontalalignment = 'center',
                    verticalalignment = 'center')

            def step(i):  
                    im.set_array(maze_to_matrix(_mazes[i]))
                    return([im])
    
            ani = animation.FuncAnimation(
                fig, 
                step, 
                frames = len(_mazes),
                repeat = repeat
            )

            plt.close()

            if fileName is not None:
                ani.save(fileName,writer='ffmeg')
            return ani
if __name__ == "__main__":
    welcome()
# numpy comparison warnings
