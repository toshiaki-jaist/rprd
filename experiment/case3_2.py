from z3 import *
from gcpd import *

case32 = Model()
case32.num_model = 10
case32.max_step = 9

case32.set_car(["EgoCar", "LCar", "RCar1", "RCar2"])
case32.append_box ([("EgoCar", n) for n in range(8)] + [("LCar", n) for n in range(4)] + [("RCar1", n) for n in range(6)] + [("RCar2", 0), ("RCar2", 1), ("RCar2", 2), ("RCar2", 3)])
case32.append_position ([("EgoCar", 0, 0), ("EgoCar", 1, 1), ("EgoCar", 2, 3), ("EgoCar", 3, 8), ("EgoCar", 4, 5), ("EgoCar", 5, 8), ("EgoCar", 6, 8), ("EgoCar", 7, 4)])
case32.append_position ([("LCar", 0, 3), ("LCar", 1, 7), ("LCar", 2, 8), ("LCar", 3, 9)])
case32.append_position ( [("RCar1", 0, 0), ("RCar1", 1, 2), ("RCar1", 2, 4), ("RCar1", 3, 6), ("RCar1", 4, 8), ("RCar1", 5, 9)])
case32.append_position ([("RCar2", 0, -1), ("RCar2", 1, 8), ("RCar2", 2, 7), ("RCar2", 3, 5)])
case32.append_lane ([("LCar", n, 0) for n in range(4)])
case32.append_lane ([("RCar1", n, 2) for n in range(6)])
case32.append_lane ([("RCar2", 0, 2), ("RCar2", 1, 2),("RCar2", 2, 2),("RCar2", 3, 2)])
case32.append_lane ([("EgoCar", 0, 0), ("EgoCar", 1, 0), ("EgoCar", 2, 1), ("EgoCar", 3, 2), ("EgoCar", 4, 1), ("EgoCar", 5, 1), ("EgoCar", 6, 0), ("EgoCar", 7, 0)])
case32.set_init ([("EgoCar", 0), ("LCar", 0), ("RCar1", 0), ("RCar2", 0)])
case32.append_ntrans ([("EgoCar", 1, "EgoCar", 2)])
case32.append_ntrans ([("LCar", 0, "LCar", 1), ("LCar", 0, "LCar", 2), ("LCar", 0, "LCar", 3)])
case32.append_ntrans ([("RCar1", 0, "RCar1", 1), ("RCar1", 1, "RCar1", 2), ("RCar1", 2, "RCar1", 3), ("RCar1", 2, "RCar1", 4), ("RCar1", 2, "RCar1", 5)])
case32.append_ctrans ([("RCar2", 0, "RCar2", 1, "RCar1", 5), ("RCar2", 0, "RCar2", 2, "RCar1", 4), ("RCar2", 0, "RCar2", 3, "RCar1", 3)])
case32.append_ctrans ([("EgoCar", 0, "EgoCar", 1, "RCar1", 1), ("EgoCar", 2, "EgoCar", 4, "RCar1", 4), ("EgoCar", 4, "EgoCar", 5, "LCar", 2)])
case32.append_netrans ([("EgoCar", 0, "EgoCar", 7, "RCar1", 1)])
case32.append_netrans ([("EgoCar", 2, "EgoCar", 3, "RCar1", 4)])
case32.append_netrans ([("EgoCar", 4, "EgoCar", 6, "LCar", 2)])
case32.append_netrans ([("EgoCar", 0, "EgoCar", 7, "RCar1", 1)])

if True:
    # count the number of collision scenarios
    add_constraints(case32)
    add_col(case32)
    print (s_count(case32))
elif True:
    # count the number of all scenarios
    print (s_count(case32))
else:
    # print scenarios
    pretty_print (s_gen(case32))

#collision: 325
#all: 1038
