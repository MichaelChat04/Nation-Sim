import numpy as np
import matplotlib.pyplot as plt

def generate_map(width=100, height=100):
    """Generates a random procedural terrain map."""
    noise = np.random.rand(height, width)
    elevation = np.clip(noise * 255, 0, 255)
    return elevation

def save_map_image(elevation, filename='static/map.png'):
    """Saves the generated terrain map as an image."""
    plt.imshow(elevation, cmap='terrain')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_and_save_map():
    """Generates a new map and saves it."""
    elevation = generate_map()
    save_map_image(elevation)
    return "/static/map.png"
