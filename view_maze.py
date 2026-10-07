import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("maze.xml")
data = mujoco.MjData(model)

print("MuJoCo maze loaded successfully.")
print("Close the viewer window to exit.")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)