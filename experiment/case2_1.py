from z3 import *
from gcpd import *

case21 = Model()
case21.num_model = 10
case21.max_step = 8
case21.set_car (["EgoCar", "LCar", "RCar"])
case21.append_box ([("EgoCar", n) for n in range(8)] + [("LCar", n) for n in range(4)] + [("RCar", n) for n in range(6)])
case21.append_position([("EgoCar", 0, 0), ("EgoCar", 1, 1), ("EgoCar", 2, 3), ("EgoCar", 3, 8), ("EgoCar", 4, 5), ("EgoCar", 5, 8), ("EgoCar", 6, 8), ("EgoCar", 7, 4)])
case21.append_position([("LCar", 0, 3), ("LCar", 1, 7), ("LCar", 2, 8), ("LCar", 3, 9)])
case21.append_position([("RCar", 0, 0), ("RCar", 1, 2), ("RCar", 2, 4), ("RCar", 3, 6), ("RCar", 4, 8), ("RCar", 5, 9)])
case21.append_lane ([("LCar", n, 0) for n in range(4)])
case21.append_lane ([("RCar", n, 2) for n in range(6)])
case21.append_lane ([("EgoCar", 0, 0), ("EgoCar", 1, 0), ("EgoCar", 2, 1), ("EgoCar", 3, 2), ("EgoCar", 4, 1), ("EgoCar", 5, 1), ("EgoCar", 6, 0), ("EgoCar", 7, 0)])
case21.set_init([("EgoCar", 0), ("LCar", 0), ("RCar", 0)])

case21.append_ntrans ([("LCar", 0, "LCar", 1), ("LCar", 0, "LCar", 2), ("LCar", 0, "LCar", 3)])
case21.append_ntrans ([("EgoCar", 2, "EgoCar", 4)])
case21.append_ntrans ([("RCar", 0, "RCar", 1), ("RCar", 2, "RCar", 3), ("RCar", 2, "RCar", 4)])
case21.append_ctrans ([("EgoCar", 0, "EgoCar", 1, "RCar", 1), ("EgoCar", 4, "EgoCar", 6, "LCar", 3)])
case21.append_netrans ([("EgoCar", 0, "EgoCar", 7, [("RCar", 1)]), ("EgoCar", 4, "EgoCar", 5, [("LCar", 3)])])
case21.append_strans ([[("EgoCar", 1, "EgoCar", 2), ("RCar", 1, "RCar", 2)], [("EgoCar", 2, "EgoCar", 3), ("RCar", 2, "RCar", 5)]])

if True:
    # count the number of collision scenarios
    add_constraints(case21)
    add_col(case21)
    print (s_count(case21))
elif True:
    # count the number of all scenarios
    print (s_count(case21))
else:
    # print scenarios
    pretty_print (s_gen(case21))

#all: 150
#collision: 0
