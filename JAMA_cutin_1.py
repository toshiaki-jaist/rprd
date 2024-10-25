from z3 import *
from gcpd import *
from PIL import Image, ImageDraw, ImageFont
from gcpd_gif import *

cutin = Model()
cutin.num_model = 3
cutin.max_step = 5
cutin.set_car(["Ego", "Other"])
for i in range(3):
    cutin.add_box(("Ego", i))
    cutin.add_position(("Ego", i, i))
    cutin.add_lane(("Ego", i, 0))
  
for i in range(6):
    cutin.add_box(("Other", i))
cutin.append_position([("Other", 0, 2), ("Other", 1, 2), ("Other", 2, 1)])
cutin.append_position([("Other", 3, 1), ("Other", 4, 0), ("Other", 5, 0)])
cutin.append_lane([("Other", 0, 1), ("Other", 1, 0), ("Other", 2, 1)])
cutin.append_lane([("Other", 3, 0), ("Other", 4, 1), ("Other", 5, 0)])

cutin.set_init ([("Ego", 0), ("Other", 0)])
cutin.add_ntrans(("Ego", 0, "Ego", 1))
cutin.add_ntrans(("Ego", 1, "Ego", 2))
cutin.add_ntrans(("Other", 0, "Other", 1))
cutin.add_ntrans(("Other", 0, "Other", 2))
cutin.add_ntrans(("Other", 2, "Other", 3))
cutin.add_ntrans(("Other", 2, "Other", 4))
cutin.add_ntrans(("Other", 3, "Other", 5))
cutin.add_ntrans(("Other", 4, "Other", 5))

vg = VehicleGif()
vg.car_color = {'Ego': (0, 255, 0), 'Other': (255, 0, 0)}
vg.x_margin= {'Ego': 20, 'Other': 50}
vg.y_margin= {'Ego': 20, 'Other': 90}
vg.y_bup = 0
vg.grid_x = 2
vg.grid_y = 3

add_constraints(cutin)
#add_solver(Not(eval_col(cutin,  lambda c1, c2, bx, t: ps_col(c1, c2, bx, t))))
add_solver(eval_col(cutin,  lambda c1, c2, bx, t: ps_col(c1, c2, bx, t)))
add_constraints_tm(cutin, lambda bx, t: ps_col("Other", "Ego", bx, t))

if True: 
    hss = enum_ss(cutin)
#    vg.gen_gif(hss, "cutin_gif")
    vg.gen_gif_all(hss, "cutin_gif")
else:
    print(enum_count(cutin))

#total 23
#no collision 12
#collision 11
#collision(tm) 3
