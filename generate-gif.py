import os
import random
from PIL import Image, ImageDraw, ImageEnhance
import imageio

# Path to the folder containing the images
image_folder = 'gif-animation-images'

# List all images in the folder
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Create a list to store the frames
frames = []

# Define the size of the GIF
gif_width = 800
gif_height = 800
frame_count = 100  # Number of frames in the GIF
duration_per_frame = 30 / len(images)  # Duration of each frame to make it 10 seconds

# Create a base frame
base_frame = Image.new('RGBA', (gif_width, gif_height), (255, 255, 255, 0))

# Create frames
for img_path in images:
    frame = base_frame.copy()
    img = Image.open(img_path).convert('RGBA')
    img = img.resize((500, 500))  # Resize to a larger size for better visualization

    # Apply random rotation
    rotated_img = img.rotate(random.uniform(0, 360), expand=1)

    # Center position
    x = (gif_width - rotated_img.width) // 2
    y = (gif_height - rotated_img.height) // 2

    frame.paste(rotated_img, (x, y), rotated_img)
    frames.append(frame)

# Save the frames as a GIF
output_path = 'overlay_images.gif'
frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=int(duration_per_frame * 1000), loop=0)

print(f"GIF saved at {output_path}")