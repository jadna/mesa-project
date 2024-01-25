
# Multi-agent Project

Project carried out for the disciplines of Multiagent Systems and Advanced Modeling and Simulation Methods.
The system has three routes, where each route has a minimum time and a capacity for simultaneous cars.
Agents must choose which route to use according to the number of cars that are already using the route and their capacity, agents have their entry and exit times on the routes.

Q-Leraning was used so that agents learn to make their decisions by interacting directly with the environment, without the need for prior knowledge or human supervision. For this reason, Q-Learning is widely applied in solving complex and dynamic problems.


## Installation

To install dependencies

```bash
  pip install -r requirements.txt
```

## Run the project

To run the project, go to the folder

```bash
  mesa-project/mams-project/
```

And run the command

```bash
  python model.py
```
    
## Simulation
For the simulation, three scenarios were used.
Each route has an origin and destination, a capacity, minimum time and volume (number of cars using the route).

However, for the simulation, the city of Porto was used to indicate three different scenarios, with origin, destination and real distances.

To calculate the capacity of a route, we define that it will be calculated by the size of the route (according to Google maps) divided by the average length of a car.

Average length of a car is: 4.45 meters

$` \frac{route\_size}{average\_car\_length} `$


The minimum time was used using the time provided by Google maps, according to the origin and destination.

The calculation to define the route capacity was route size (m)/average length of a car (m)

### Scenario 1

FEUP -> Casa da Música, Av. da Boavista

Route 1: 3.6 KM (3600 m) -> 12 min ---------- Capacity: 808

Route 2: 6.5 KM (6500 m) -> 13 min ---------- Capacity: 1460

Route 3: 4.2 km (4200 m) -> 14 min ---------- Capacity: 943


### Scenario 2

FEUP -> Trindade

Route 1: 2.5 KM (2500 m) -> 8 min ---------- Capacity: 561

Route 2: 2.6 KM (2600 m) -> 9 min ---------- Capacity: 584

Route 3: 2.7 km (2700 m) -> 11 min ---------- Capacity: 606


### Scenario 3

FEUP -> Rua Visconde de bóbeda

Route 1: 3.5 KM (3500 m) -> 13 min ---------- Capacity: 786

Route 2: 3.6 KM (3600 m) -> 14 min ---------- Capacity: 808

Route 3: 4.0 km (4000 m) -> 15 min ---------- Capacity: 898




