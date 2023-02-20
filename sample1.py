from z3 import *
from gcpd import *

my_first_model = Model()
my_first_model.num_model = 5
my_first_model.max_step = 2
my_first_model.set_car(["LCar", "RCar"])
my_first_model.append_box ([("LCar", 0), ("LCar", 1)])
my_first_model.append_box ([("RCar", 0), ("RCar", 1)])
my_first_model.append_position([("LCar", 0, 0), ("LCar", 1, 1)])
my_first_model.append_position([("RCar", 0, 0), ("RCar", 1, 1)])
my_first_model.append_lane ([("LCar", 0, 0), ("LCar", 1, 0)])
my_first_model.append_lane ([("RCar", 0, 1), ("RCar", 1, 1)])
my_first_model.set_init ([("LCar", 0), ("RCar", 0)])
my_first_model.add_ntrans (("LCar", 0, "LCar", 1))
my_first_model.add_ntrans (("RCar", 0, "RCar", 1))
pretty_print(s_gen(my_first_model))
