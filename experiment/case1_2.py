from z3 import *
from gcpd import *

case12 = Model()
case12.num_model = 30
case12.max_step = 6

case12.set_car (["LCar", "RCar"])
case12.append_box([("LCar", n) for n in range(5)] + [("RCar", n) for n in range(6)])
case12.append_position([("LCar", 0, 0), ("RCar", 0, 0), ("LCar", 1, 1), ("RCar", 1, 2), ("LCar", 2, 3), ("RCar", 2, 4), ("RCar", 3, 5), ("RCar", 4, 6), ("LCar", 3, 6), ("RCar", 5, 7), ("LCar", 4, 5)])
case12.append_lane([("RCar", n, 2) for n in range(5)])
case12.append_lane([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 4, 0), ("LCar", 2, 1), ("LCar", 3, 2)])
case12.set_init ([("LCar", 0), ("RCar", 0)])
case12.append_ntrans([("LCar", 1, "LCar", 2), ("LCar", 2, "LCar", 3)])
case12.append_ntrans([("RCar", 0, "RCar", 1), ("RCar", 1, "RCar", 2), ("RCar", 2, "RCar", 3), ("RCar", 2, "RCar", 4), ("RCar", 2, "RCar", 5)])
case12.append_ntrans([("LCar", 0, "LCar", 1), ("LCar", 0, "LCar", 4)])

if True:
    # count the number of collision scenarios
    add_constraints(case12)
    add_col(case12)
    print (s_count(case12))
elif True:
    # count the number of all scenarios
    print (s_count(case12))
else:
    # print scenarios
    pretty_print (s_gen(case12))

#all: 72
#collision: 20
