import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from datetime import datetime


def update_game_of_life(state, width, height):
    """Updates the Game of Life state with wraparound and 8-bit states."""
    padded_state = np.pad(state, ((1, 1), (1, 1)), mode='wrap')
    neighborhood_sums = (
        padded_state[:-2, :-2] + padded_state[:-2, 1:-1] + padded_state[:-2, 2:] +
        padded_state[1:-1, :-2]                     + padded_state[1:-1, 2:] +
        padded_state[2:, :-2] + padded_state[2:, 1:-1] + padded_state[2:, 2:]
    )

    # Apply modified Game of Life rules for 8-bit states
    new_state = np.zeros_like(state, dtype=np.uint8)
    alive_mask = (state > 0)
    birth_mask = (neighborhood_sums == 128)  # Example birth condition (experiment!)
    survive_mask = (neighborhood_sums >= 64) & (neighborhood_sums <= 192) & alive_mask # Example survival condition (experiment!)

    new_state[birth_mask] = 128  # Birth with initial energy
    new_state[survive_mask] = np.clip(state[survive_mask] - 1, 0, 255)  # Energy decay

    #Optional: Diffusion of energy to neighbors
    for i in range(height):
        for j in range(width):
            if new_state[i, j] > 0:  # If cell is alive
                neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                for x, y in neighbors:  # For each neighbor
                    x = x % height  # Wraparound for boundary conditions
                    y = y % width
                    new_state[x, y] = min(255, new_state[x, y] + 1)  # Transfer some energy

    return new_state

# Get user input for noise level
while True:
    try:
        noise_level = float(input("Enter noise level (0.0 to 1): "))
        if 0.0 <= noise_level <= 1:
            break
        else:
            print("Invalid input. Please enter a value between 0.0 and 1.0.")
    except ValueError:
        print("Invalid input. Please enter a numerical value.")
        
def update(frame, ims, states, width, height, noise_level):
    artists = []
    for i, (im, state) in enumerate(zip(ims, states)):
        noise = np.random.rand(height, width) < noise_level
        state[:, :] = update_game_of_life(state, width, height) + noise
        im.set_array(state)
        artists.append(im)
    return artists

# Setup parameters
width, height = 64, 64
noise_level = 0.000
max_values = [16, 32, 64, 128]

# Create figure and subplots
fig, axs = plt.subplots(1, 4, figsize=(12, 4))
fig.suptitle('8-bit Game of Life: Seed maximum health = 192')

# Initialize states and images
states = []
ims = []
for i, max_val in enumerate(max_values):
    # Create initial state
    state = np.random.randint(max_val, 192, (height, width), dtype=np.uint8)
    states.append(state)
    
    # Setup plot
    im = axs[i].imshow(state, cmap='inferno', interpolation='nearest')
    axs[i].set_title(f'Min Value: {max_val}')
    ims.append(im)

# Create animation
ani = FuncAnimation(
    fig, update, fargs=(ims, states, width, height, noise_level),
    frames=100, interval=10, blit=True, repeat=False
)

# Save the GIF
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"ca_grid_{timestamp}.gif"
writer = PillowWriter(fps=24)
ani.save(filename, writer=writer)
print(f"GIF saved as: {filename}")

plt.tight_layout()
plt.show()
