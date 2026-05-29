import numpy as np
from PIL import Image

def generate_terrain(filename, size=513):
    # Create an empty array
    terrain = np.zeros((size, size))
    
    # Generate some simple hills and valleys using sine waves
    x = np.linspace(0, 4 * np.pi, size)
    y = np.linspace(0, 4 * np.pi, size)
    X, Y = np.meshgrid(x, y)
    
    # Combination of waves for "hilly" terrain
    Z = np.sin(X) * np.cos(Y) * 20.0  # Big rolling hills
    Z += np.sin(X * 2.5) * np.cos(Y * 2.5) * 5.0  # Smaller bumps
    Z += np.sin(X * 0.5) * 15.0 # A slope
    
    # Normalize to 0-255
    Z_min = Z.min()
    Z_max = Z.max()
    Z_norm = (Z - Z_min) / (Z_max - Z_min) * 255.0
    
    # Convert to 8-bit unsigned integer
    Z_img = Z_norm.astype(np.uint8)
    
    # Save as PNG
    img = Image.fromarray(Z_img)
    img.save(filename)
    print(f"Successfully generated {filename} with size {size}x{size}")

if __name__ == "__main__":
    generate_terrain('terrain.png')
