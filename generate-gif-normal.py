import os
from PIL import Image
import imageio

# Path to the folder containing the images
image_folder = 'C://Users//O//Desktop//Master Thesis//0A_images//New folder//Series-004'

# List all images in the folder
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Create a list to store the frames
frames = []

# Define the size of the GIF
gif_width = 400
gif_height = 400
frame_count = 100  # Number of frames in the GIF
duration_per_frame = 10  # Duration of each frame in milliseconds

base_frame = Image.new('RGBA', (gif_width, gif_height), (255, 255, 255, 0))

# Create frames
for img_path in images:
    frame = base_frame.copy()
    img = Image.open(img_path).convert('RGBA')

    # Resize image while maintaining aspect ratio
    img.thumbnail((264, 384))

    # Center position
    x = (gif_width - img.width) // 2
    y = (gif_height - img.height) // 2

    frame.paste(img, (x, y), img)
    frames.append(frame)

# Save the frames as a GIF
output_path = '3d-gre-video.gif'
frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=duration_per_frame, loop=0)

print(f"GIF saved at {output_path}")