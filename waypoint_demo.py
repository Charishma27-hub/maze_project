import time

import mujoco
import mujoco.viewer

from waypoints import get_astar_waypoints


MODEL_FILE = "maze.xml"

WAYPOINT_TOLERANCE = 0.08
MOVE_SPEED = 0.5


def main():

    model = mujoco.MjModel.from_xml_path(MODEL_FILE)
    data = mujoco.MjData(model)

    waypoints = get_astar_waypoints()

    body_id = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_BODY,
        "navigator",
    )

    if body_id == -1:
        raise RuntimeError("Could not find navigator body.")

    mocap_id = model.body_mocapid[body_id]

    if mocap_id == -1:
        raise RuntimeError("Navigator is not a mocap body.")

    print("Starting waypoint navigation...")
    print("Number of waypoints:", len(waypoints))

    waypoint_index = 0

    # Put the navigator exactly at the A* start.
    start_x, start_y = waypoints[0]
    data.mocap_pos[mocap_id] = [start_x, start_y, 0.30]

    with mujoco.viewer.launch_passive(model, data) as viewer:

        viewer.cam.lookat[:] = [4.0, 2.0, 0.0]
        viewer.cam.distance = 8.0
        viewer.cam.azimuth = 90
        viewer.cam.elevation = -60

        while viewer.is_running():

            if waypoint_index >= len(waypoints):
                print("Reached goal!")
                time.sleep(2)
                break

            target_x, target_y = waypoints[waypoint_index]

            current_x = data.mocap_pos[mocap_id][0]
            current_y = data.mocap_pos[mocap_id][1]

            dx = target_x - current_x
            dy = target_y - current_y

            distance = (dx * dx + dy * dy) ** 0.5

            if distance < WAYPOINT_TOLERANCE:

                print(
                    f"Reached waypoint {waypoint_index}: "
                    f"({target_x:.2f}, {target_y:.2f})"
                )

                waypoint_index += 1

                time.sleep(0.4)

                continue

            vx = MOVE_SPEED * dx / max(distance, 1e-8)
            vy = MOVE_SPEED * dy / max(distance, 1e-8)

            new_x = current_x + vx * 0.02
            new_y = current_y + vy * 0.02

            data.mocap_pos[mocap_id] = [
                new_x,
                new_y,
                0.30,
            ]

            mujoco.mj_forward(model, data)

            viewer.sync()

            time.sleep(0.02)

        print("Navigation finished.")


if __name__ == "__main__":
    main()