from pathlib import Path

from maze_generator import MAZE, get_start_and_goal


CELL_SIZE = 1.0
WALL_HEIGHT = 0.5
FLOOR_THICKNESS = 0.05


def grid_to_world(row, col, rows):
    x = col * CELL_SIZE
    y = (rows - 1 - row) * CELL_SIZE
    return x, y


def generate_xml():
    rows, cols = MAZE.shape
    start, goal = get_start_and_goal(MAZE)

    xml = f"""<mujoco model="a1_maze">

    <compiler angle="radian" coordinate="local"/>

    <option gravity="0 0 -9.81" timestep="0.002"/>

    <visual>
        <headlight diffuse="0.8 0.8 0.8"
                   ambient="0.3 0.3 0.3"/>
    </visual>

    <asset>

        <texture name="floor_texture"
                 type="2d"
                 builtin="checker"
                 width="512"
                 height="512"
                 rgb1="0.75 0.75 0.75"
                 rgb2="0.55 0.55 0.55"/>

        <material name="floor_material"
                  texture="floor_texture"
                  texrepeat="5 5"/>

        <material name="wall_material"
                  rgba="0.2 0.2 0.2 1"/>

        <material name="start_material"
                  rgba="0 0.8 0 1"/>

        <material name="goal_material"
                  rgba="0.8 0.8 0 1"/>

    </asset>

    <worldbody>

        <!-- Virtual navigator used to test waypoint following -->
       <body name="navigator" mocap="true" pos="0 4 0.30">

         <geom name="navigator_geom"
          type="sphere"
          size="0.25"
          rgba="0 0 1 1"
          contype="0"
          conaffinity="0"/>

        </body>
        <!-- Floor -->
        <geom name="floor"
              type="box"
              size="{cols * CELL_SIZE / 2} {rows * CELL_SIZE / 2} {FLOOR_THICKNESS}"
              pos="{(cols - 1) * CELL_SIZE / 2} {(rows - 1) * CELL_SIZE / 2} {-FLOOR_THICKNESS}"
              material="floor_material"
              contype="1"
              conaffinity="1"/>
"""

    wall_id = 0

    for row in range(rows):
        for col in range(cols):

            if MAZE[row, col] != 1:
                continue

            x, y = grid_to_world(row, col, rows)

            xml += f"""
        <geom name="wall_{wall_id}"
              type="box"
              size="{CELL_SIZE / 2} {CELL_SIZE / 2} {WALL_HEIGHT / 2}"
              pos="{x} {y} {WALL_HEIGHT / 2}"
              material="wall_material"
              contype="1"
              conaffinity="1"/>
"""

            wall_id += 1

    start_x, start_y = grid_to_world(start[0], start[1], rows)

    xml += f"""
        <!-- Start marker -->
        <geom name="start_marker"
              type="cylinder"
              size="0.25 0.01"
              pos="{start_x} {start_y} 0.01"
              material="start_material"
              contype="0"
              conaffinity="0"/>
"""

    goal_x, goal_y = grid_to_world(goal[0], goal[1], rows)

    xml += f"""
        <!-- Goal marker -->
        <geom name="goal_marker"
              type="cylinder"
              size="0.25 0.01"
              pos="{goal_x} {goal_y} 0.01"
              material="goal_material"
              contype="0"
              conaffinity="0"/>

    </worldbody>

</mujoco>
"""

    output_path = Path("maze.xml")
    output_path.write_text(xml, encoding="utf-8")

    print(f"Generated: {output_path}")
    print(f"Grid size: {rows} x {cols}")
    print(f"Walls: {wall_id}")
    print(f"Start world position: ({start_x:.2f}, {start_y:.2f})")
    print(f"Goal world position: ({goal_x:.2f}, {goal_y:.2f})")


if __name__ == "__main__":
    generate_xml()