import matplotlib.pyplot as plt

from maze_generator import MAZE, get_start_and_goal
from astar import astar


def plot_maze(maze, path=None):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw walls and free space
    ax.imshow(
        maze,
        cmap="gray_r",
        origin="upper"
    )

    # Draw A* path
    if path:
        rows = [p[0] for p in path]
        cols = [p[1] for p in path]

        ax.plot(
            cols,
            rows,
            marker="o",
            linewidth=3,
            markersize=6
        )

    # Start and goal
    start, goal = get_start_and_goal(maze)

    ax.scatter(
        start[1],
        start[0],
        marker="o",
        s=200,
        label="Start"
    )

    ax.scatter(
        goal[1],
        goal[0],
        marker="*",
        s=300,
        label="Goal"
    )

    ax.set_xticks(range(maze.shape[1]))
    ax.set_yticks(range(maze.shape[0]))

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title("A* Maze Path")

    ax.grid(True)
    ax.legend()

    plt.tight_layout()

    output_file = "astar_path.png"
    plt.savefig(output_file, dpi=150, bbox_inches="tight")

    print(f"Visualization saved to: {output_file}")


def main():

    start, goal = get_start_and_goal(MAZE)

    path = astar(
        MAZE,
        start,
        goal
    )

    if path is None:
        print("No path found.")
        return

    print("Start:", start)
    print("Goal:", goal)
    print("Path length:", len(path))

    plot_maze(MAZE, path)


if __name__ == "__main__":
    main()