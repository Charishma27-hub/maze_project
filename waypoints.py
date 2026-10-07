from maze_generator import MAZE, get_start_and_goal
from astar import astar


CELL_SIZE = 1.0


def grid_to_world(row, col, rows):
    """
    Convert maze grid coordinates to MuJoCo x, y coordinates.
    """
    x = col * CELL_SIZE
    y = (rows - 1 - row) * CELL_SIZE
    return x, y


def get_astar_waypoints():
    """
    Compute the A* path and convert every grid cell
    into MuJoCo world coordinates.
    """
    rows, cols = MAZE.shape

    start, goal = get_start_and_goal(MAZE)
    path = astar(MAZE, start, goal)

    if path is None:
        raise RuntimeError("A* could not find a path.")

    waypoints = []

    for row, col in path:
        x, y = grid_to_world(int(row), int(col), rows)
        waypoints.append((x, y))

    return waypoints


if __name__ == "__main__":
    waypoints = get_astar_waypoints()

    print("A* waypoints:")
    for i, (x, y) in enumerate(waypoints):
        print(f"{i:2d}: x={x:.2f}, y={y:.2f}")

    print()
    print("Number of waypoints:", len(waypoints))