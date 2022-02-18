# rprd
### NAME
GRPRD: scenario Generator for Road Position Relation Diagram
### Overview
RPRD is a diagram for modeling vehicle positions, which is the extenstion of UML activity diagram. RPRD allows us to represent a large
number of scenarios as a compact model. GRPRD is a tool to generate such scenarios from a RPRD model based on the SAT/SMT solver Z3. 
### Usage
Installing Z3 and Z3py is required to run GRPRD. A RPRD model is described as a python program. Importing 'road_gen.py' in the program and running it generate scenarios.

Firstly, it is necessary to import z3py and GRPRD.
```
from z3 import *
from road_gen import *
```
Then, make a model instance.
```
my_first_model = Model()
```
The maximal numbers of scenarios and steps of each scenario is set to the variables `num_model` and `max_step` of the instance respectively as follows.
```
my_first_model.num_model = 5
my_first_model.max_step = 2
```
Model elements are added to the model instance. Names of the model elements are represented as strings. 
```
set_car (["car1", "car2", ...])
append_box ([("car1", 0), ("car2", 1), ...])
append_position ([("car1", 0, 0), ("car2", 1, 1), ...])
append_lane ([("car1", 0, 0), ("car1", 1, 0), ...])
set_init([("car1", 0), ("car2", 0)])
add_ntrans(("car1", 0, "car1", 1))
```
`append_box` adds boxes to the model. A box is represented as a pair of a string and integer which represent a car and box ID, respectively. 
`append_position` adds box positions to the model. A box position is represented as a tuple of a string, integer, and integer which represent a car, box ID, and a position, respectively. 
A lane is represented as an integer. `append_lane` gets a tuple of string, integer, integer which represent a car, a box, and a lane, respectively, and assign the car to the lane. 
`set_init` defines inital boxes of cars.
`add_ntrans` adds a normal transition of boxes to the model. The transition is represented as a pair of a source box and destination box. Note that each box is represented as a pair of a car and box ID. 
