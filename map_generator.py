import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import noise
import random
import json
from scipy.spatial import Voronoi

# Map settings
MAP_WIDTH = 512
MAP_HEIGHT = 512
NUM_REGIONS = 50  # Controls the number of landmasses
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0
SEED = random.randint(0, 10000)

# Generate Perlin noise-based landmass mask (for realistic continents)
def generate_landmass_mask():
    mask = np.zeros((MAP_WIDTH, MAP_HEIGHT))
    scale = 150.0  # Larger scale for continents
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            nx = x / MAP_WIDTH - 0.5
            ny = y / MAP_HEIGHT - 0.5
            distance = np.sqrt(nx * nx + ny * ny) * 2.0  # Circular landmass shape
            elevation = noise.pnoise2(x / scale, y / scale, octaves=OCTAVES, 
                                      persistence=PERSISTENCE, lacunarity=LACUNARITY, 
                                      repeatx=MAP_WIDTH, repeaty=MAP_HEIGHT, base=SEED)
            mask[x][y] = elevation - distance  # Subtract distance to keep edges ocean
    return mask

# Generate Voronoi regions for major landmass structures
def generate_voronoi_regions():
    points = np.random.rand(NUM_REGIONS, 2) * [MAP_WIDTH, MAP_HEIGHT]
    vor = Voronoi(points)
    return vor, points

# Generate Perlin noise-based heightmap
def generate_heightmap(landmass_mask, vor, points):
    world = np.zeros((MAP_WIDTH, MAP_HEIGHT))
    scale = 75.0  # Smaller scale for finer terrain features
    offset_x = random.uniform(-500, 500)
    offset_y = random.uniform(-500, 500)

    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            region_index = np.argmin(np.linalg.norm(points - np.array([x, y]), axis=1))
            base_elevation = noise.pnoise2(
                (x + offset_x) / scale, (y + offset_y) / scale, 
                octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY, 
                repeatx=MAP_WIDTH, repeaty=MAP_HEIGHT, base=SEED
            )
            world[x][y] = base_elevation + landmass_mask[x][y]  # Apply landmass mask
    return world

# Classify biomes based on height
def generate_biomes(heightmap):
    biomes = np.full((MAP_WIDTH, MAP_HEIGHT), "ocean", dtype=object)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            height = heightmap[x][y]
            if height < -0.2:
                biomes[x][y] = "deep_ocean"
            elif height < -0.05:
                biomes[x][y] = "coastal_ocean"
            elif height < 0.05:
                biomes[x][y] = "beach"
            elif height < 0.3:
                biomes[x][y] = "grassland"
            elif height < 0.5:
                biomes[x][y] = "forest"
            elif height < 0.7:
                biomes[x][y] = "hills"
            elif height < 0.9:
                biomes[x][y] = "mountains"
            else:
                biomes[x][y] = "snow"
    return biomes

# Generate a procedural world
def generate_world():
    landmass_mask = generate_landmass_mask()
    vor, points = generate_voronoi_regions()
    heightmap = generate_heightmap(landmass_mask, vor, points)
    biomes = generate_biomes(heightmap)
    return heightmap, biomes

# Save world data
def save_world(heightmap, biomes):
    data = {
        "heightmap": heightmap.tolist(),
        "biomes": biomes.tolist()
    }
    with open("world_data.json", "w") as f:
        json.dump(data, f)

# Visualize world map
def visualize_world(heightmap, biomes):
    colors = {
        "deep_ocean": "#003366",
        "coastal_ocean": "#004488",
        "beach": "#EEDDAA",
        "grassland": "#66AA44",
        "forest": "#228B22",
        "hills": "#8B7765",
        "mountains": "#555555",
        "snow": "#FFFFFF"
    }
    img = np.zeros((MAP_WIDTH, MAP_HEIGHT, 3))
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            biome = biomes[x][y]
            img[x, y] = mcolors.to_rgb(colors[biome])
    plt.imshow(img)
    plt.axis("off")
    plt.savefig("static/world_map.png", dpi=300)
    plt.show()

# Main execution
if __name__ == "__main__":
    heightmap, biomes = generate_world()
    save_world(heightmap, biomes)
    visualize_world(heightmap, biomes)
