import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
grid_size = (100, 100)  # represent graphene as a 100x100 lattice of carbon atoms
n_atoms = grid_size[0] * grid_size[1]
n_particles = 1000  # number of incident particles for each simulation

# Define energy levels (in GeV)
energies = [5, 15]

# Define particle types with an arbitrary "damage efficiency" factor.
# These factors are not from exact physical data but serve to differentiate the particle types.
particles = {
    "proton": 1.0,
    "electron": 0.5,
    "muon": 0.8
}

# A simplified model for the displacement probability:
# We assume the probability of displacement scales with the energy and the particle-specific efficiency.
# For a given particle of energy E (in GeV), the displacement probability might be:
#   P_disp = efficiency * (E / E_max)
# where E_max is an arbitrary normalization constant (here we take E_max = 15 GeV).
E_max = 15.0

def simulate_damage(particle_type, energy, n_particles, grid_size):
    efficiency = particles[particle_type]
    # The displacement probability for each particle:
    p_disp = efficiency * (energy / E_max)
    
    # Initialize a lattice that counts the number of displacements per atom.
    lattice = np.zeros(grid_size, dtype=int)
    
    # For each incident particle, choose a random target atom.
    for _ in range(n_particles):
        # Randomly select an atom in the grid
        i = np.random.randint(0, grid_size[0])
        j = np.random.randint(0, grid_size[1])
        
        # Determine if this impact displaces the atom.
        if np.random.rand() < p_disp:
            lattice[i, j] += 1  # record a defect event (or multiple events if same site hit repeatedly)
            
    return lattice

def plot_lattice(lattice, title):
    plt.figure(figsize=(6,5))
    plt.imshow(lattice, cmap='hot', interpolation='nearest')
    plt.colorbar(label="Number of defects")
    plt.title(title)
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.show()

# Run simulations for each particle type and energy, and display total damage.
results = {}
for particle in particles.keys():
    for energy in energies:
        lattice = simulate_damage(particle, energy, n_particles, grid_size)
        total_defects = np.sum(lattice)
        results[(particle, energy)] = total_defects
        title = f"{particle.capitalize()} at {energy} GeV\nTotal defects: {total_defects}"
        print(title)
        plot_lattice(lattice, title)