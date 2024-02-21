from z3 import *
from gcpd import *
from PIL import Image, ImageDraw, ImageFont
from gcpd_gif import *

sample_gif = Model()
sample_gif.num_model = 6
sample_gif.max_step = 4
sample_gif.set_car(["LCar", "RCar"])
sample_gif.append_box ([("LCar", 0), ("LCar", 1), ("LCar", 2)])
sample_gif.append_box ([("RCar", 0), ("RCar", 1), ("RCar", 2)])
sample_gif.append_position([("LCar", 0, 0), ("LCar", 1, 1), ("LCar", 2, 2)])
sample_gif.append_position([("RCar", 0, 0), ("RCar", 1, 1), ("RCar", 2, 2)])
sample_gif.append_lane ([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 2, 1)])
sample_gif.append_lane ([("RCar", 0, 1), ("RCar", 1, 1), ("RCar", 2, 0)])
sample_gif.set_init ([("LCar", 0), ("RCar", 0)])
sample_gif.add_ntrans (("LCar", 0, "LCar", 1))
sample_gif.add_ntrans (("LCar", 1, "LCar", 2))
sample_gif.add_ntrans (("RCar", 0, "RCar", 1))
sample_gif.add_ntrans (("RCar", 1, "RCar", 2))

vg = VehicleGif()
vg.car_color = {'LCar': (0, 255, 0), 'RCar': (255, 0, 0)}
vg.x_margin= {'LCar': 20, 'RCar': 50}
vg.y_margin= {'LCar': 20, 'RCar': 90}
vg.y_bup = 0
vg.grid_x = 2
vg.grid_y = 3

add_constraints(sample_gif)
hss = enum_ss(sample_gif)
vg.gen_gif(hss, "sample_gif")
vg.gen_gif_all(hss, "sample_gif")
