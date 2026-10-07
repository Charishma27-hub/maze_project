from maze_generator import MAZE, get_start_and_goal, print_maze
from astar import astar


def main():

    start, goal = get_start_and_goal(MAZE)

    path = astar(MAZE, start, goal)

    print("Original maze:")
    print_maze(MAZE)

    print()

    if path is None:
        print("No path found.")
        return

    print("A* path:")
    print(path)

    print()
    print("Maze with A* path:")
    print_maze(MAZE, path)

    print()
    print("Path length:", len(path))


if __name__ == "__main__":
    main()