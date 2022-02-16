from z3 import *
from road_gen import *
model1 = Model()
model1.num_model = 5
model1.max_step = 2
model1.set_car(["LCar", "RCar"])
model1.append_box ([("LCar", 0), ("LCar", 1)])
model1.append_box ([("RCar", 0), ("RCar", 1)])
model1.append_position([("LCar", 0, 0), ("LCar", 1, 1)])
model1.append_position([("RCar", 0, 0), ("RCar", 1, 1)])
model1.append_lane ([("LCar", 0, 0), ("LCar", 1, 0)])
model1.append_lane ([("RCar", 0, 1), ("RCar", 1, 1)])
model1.set_init ([("LCar", 0), ("RCar", 0)])
model1.add_ntrans (("LCar", 0, "LCar", 1))
model1.add_ntrans (("RCar", 0, "RCar", 1))
model1.debug_const = True
pretty_print(road_gen(model1))

solver.reset()

model2 = Model()
model2.num_model = 10
model2.max_step = 4
model2.set_car (["LCar", "RCar"])
model2.append_box([("LCar", 0), ("LCar", 1), ("LCar", 2)])
model2.append_box([("RCar", 0), ("RCar", 1), ("RCar", 2)])
model2.append_position([("LCar", 0, 0), ("LCar", 1, 1), ("LCar", 2, 2)])
model2.append_position([("RCar", 0, 0), ("RCar", 1, 1), ("RCar", 2, 2)])
model2.append_lane([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 2, 0)])
model2.append_lane([("RCar", 0, 1), ("RCar", 1, 1), ("RCar", 2, 1)])
model2.append_init([("LCar", 0), ("RCar", 0)])
model2.append_ntrans([("LCar", 0, "LCar", 1), ("LCar", 1, "LCar", 2)])
model2.append_ntrans([("RCar", 0, "RCar", 1), ("RCar", 1, "RCar", 2)])
pretty_print(road_gen(model2))

