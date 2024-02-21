from z3 import *
from gcpd import *

case11 = Model()
case11.num_model = 30
case11.max_step = 4
case11.set_car (["LCar", "RCar"])
case11.append_box ([("LCar", n) for n in range(5)] + [("RCar", n) for n in range(6)])
case11.append_position ([("LCar", 0, 0), ("RCar", 0, 0), ("LCar", 1, 1), ("RCar", 1, 2), ("LCar", 2, 3), ("RCar", 2, 4), ("RCar", 3, 5), ("RCar", 4, 6), ("LCar", 3, 6), ("RCar", 5, 7), ("LCar", 4, 5)])
case11.append_lane([("RCar", n, 2) for n in range(5)])
case11.append_lane([("LCar", 0, 0), ("LCar", 1, 0), ("LCar", 4, 0), ("LCar", 2, 1), ("LCar", 3, 2)])
case11.set_init([("LCar", 0), ("RCar", 0)])
case11.append_ntrans([("RCar", 0, "RCar", 1), ("RCar", 2, "RCar", 3), ("RCar", 2, "RCar", 4)])
case11.append_ctrans([("LCar", 0, "LCar", 1, "RCar", 1)])
case11.append_netrans([("LCar", 0, "LCar", 4, [("RCar", 1)])])
case11.append_strans ([[("LCar", 1, "LCar", 2), ("RCar", 1, "RCar", 2)], [("LCar", 2, "LCar", 3), ("RCar", 2, "RCar", 5)]])

if True: 
    pretty_print(s_gen(case11))
else:
    print (s_count (case11))

#all: 4
#collision: 0
