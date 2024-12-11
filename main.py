import os.path as osp
from wrapper_panda import PandaWrapper
from visualizer import create_viewer, add_sphere_to_viewer
from param_parser import ParamParser
from ocp import OCP
# Creating the robot
robot_wrapper = PandaWrapper(capsule=True)
rmodel, cmodel, vmodel = robot_wrapper()


path = osp.join((osp.dirname(__file__)), "scene.yaml")
scene = 1
pp = ParamParser(path, scene)
cmodel = pp.add_collisions(rmodel, cmodel)

vis = create_viewer(rmodel, cmodel, cmodel)
add_sphere_to_viewer(
    vis, "goal", 5e-2, pp.target_pose.translation, color=0x006400
)
vis.display(pp.initial_config)

ocp = OCP(rmodel, cmodel, pp.target_pose, pp.X0, pp)
problem = ocp.create_OCP()

# Problem is now created and can be solved
problem.solve()
xs_sol = problem.xs
# Display the solution

for x in xs_sol.tolist():
    vis.display(x[:rmodel.nq])
    input("Press a key to display the next state")