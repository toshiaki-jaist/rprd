from z3 import *
from gcpd import *

model1 = Model()
model1.num_model = 30
model1.max_step = 5
model1.set_car (["LCar", "RCar"])
model1.append_box ([("LCar", n) for n in range(5)] + [("RCar", n) for n in range(6)])
model1.append_position ([("LCar", 0, 0), ("RCar", 0, 0), ("LCar", 1, 1), ("RCar", 1, 2), ("LCar", 2, 3), ("RCar", 2, 4), ("RCar", 3, 5), ("RCar", 4, 6), ("LCar", 3, 6), ("RCar", 5, 7), ("LCar", 4, 5)])
model1.append_lane ([("RCar", n, 2) for n in range(5)])
model1.append_lane ([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 4, 0), ("LCar", 2, 1), ("LCar", 3, 2)])
model1.set_init([("LCar", 0), ("RCar", 0)])
model1.append_ntrans([("RCar", 0, "RCar", 1), ("RCar", 2, "RCar", 3), ("RCar", 2, "RCar", 4)])
model1.add_ctrans  (("LCar", 0, "LCar", 1, "RCar", 1))
model1.add_netrans (("LCar", 0, "LCar", 4, "RCar", 1))
model1.append_strans([[("LCar", 1, "LCar", 2), ("RCar", 1, "RCar", 2)], [("LCar", 2, "LCar", 3), ("RCar", 2, "RCar", 5)]])
pretty_print(s_gen(model1))

solver.reset()

model2 = Model()
model2.num_model = 100
model2.max_step = 6
model2.set_car (["LCar", "RCar"])
model2.append_box ([("LCar", n) for n in range(5)] + [("RCar", n) for n in range(6)])
model2.append_position ([("LCar", 0, 0), ("RCar", 0, 0), ("LCar", 1, 1), ("RCar", 1, 2), ("LCar", 2, 3), ("RCar", 2, 4), ("RCar", 3, 5), ("RCar", 4, 6), ("LCar", 3, 6), ("RCar", 5, 7), ("LCar", 4, 5)])
model2.append_lane ([("RCar", n, 2) for n in range(5)])
model2.append_lane ([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 4, 0), ("LCar", 2, 1), ("LCar", 3, 2)])
model2.set_init([("LCar", 0), ("RCar", 0)])
model2.append_ntrans([("RCar", 0, "RCar", 1), ("RCar", 2, "RCar", 3), ("RCar", 2, "RCar", 4)])
model2.append_ntrans([("LCar", 0, "LCar", 1), ("LCar", 0, "LCar", 4)])
model2.append_ntrans([("LCar", 1, "LCar", 2), ("RCar", 1, "RCar", 2), ("LCar", 2, "LCar", 3), ("RCar", 2, "RCar", 5)])
print (s_count(model2))
