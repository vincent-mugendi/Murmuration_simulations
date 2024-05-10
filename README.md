# Murmuration Simulation

[![Murmuration Simulation Screenshot](https://i.postimg.cc/zf23451Q/Screenshot-724.png)](https://postimg.cc/jWNsJp26)

This Python program simulates the flocking behavior of birds using the Pygame library. It also includes predators that chase the birds. The simulation demonstrates three main behaviors of flocking:

1. **Separation**: Birds avoid crowding by maintaining a certain distance from their neighbors.
2. **Alignment**: Birds align their direction of movement with nearby birds.
3. **Cohesion**: Birds move towards the center of mass of nearby birds.

## Getting Started

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/murmuration-simulation.git

2. Install Pygame
```pip install pygame```

3. Run the simulation
```murmuration_simulation.py```
### Customization
You can customize the simulation by adjusting the following parameters in the code:

- `NUM_BIRDS`: Number of birds in the simulation.
- `MAX_SPEED`: Maximum speed of birds.
- `MAX_FORCE`: Maximum steering force applied to birds.
- `VISION_RADIUS`: Radius within which birds perceive other birds.
- `SEPARATION_RADIUS`: Radius within which birds avoid crowding.
- `AVOID_RADIUS`: Radius within which birds avoid predators.
- `NUM_PREDATORS`: Number of predators in the simulation.
- `PREDATOR_SPEED`: Speed of predators.
- `PREDATOR_VISION_RADIUS`: Radius within which predators perceive birds.

### Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or create a pull request.

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.
