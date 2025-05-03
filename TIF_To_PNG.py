# import os
# from PIL import Image

# def convert_tif_to_png(input_folder, output_folder):
#     # Ensure output folder exists
#     os.makedirs(output_folder, exist_ok=True)
    
#     # Loop through all .tif files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(".tif"):
#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_folder, filename.replace(".tif", ".png"))
            
#             # Open and convert to PNG
#             with Image.open(input_path) as img:
#                 img.save(output_path, format="PNG")
#                 print(f"Converted: {filename} -> {output_path}")

# input_folder = "Input_Images"
# output_folder = "Compatible_Input"  # Replace with your actual output folder path
# convert_tif_to_png(input_folder, output_folder)

import os
import shutil
from PIL import Image

def convert_and_copy_images(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        if filename.lower().endswith(".tif"):
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_folder, output_filename)

            with Image.open(input_path) as img:
                img.save(output_path, format="PNG")
                print(f"Converted: {filename} -> {output_filename}")

        elif filename.lower().endswith(".png"):
            output_path = os.path.join(output_folder, filename)
            shutil.copy2(input_path, output_path)
            print(f"Copied: {filename} -> {output_path}")

# Set your folders
input_folder = "Input_Images"
output_folder = "Compatible_Input"

convert_and_copy_images(input_folder, output_folder)
