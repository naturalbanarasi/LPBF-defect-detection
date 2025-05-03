# !pip install numpy opencv-python scikit-image
import numpy as np
import cv2
import os
import glob
from skimage.morphology import octagon

def calculate_region_statistics(image, contours):
    """Calculate mean and variance for each contour region"""
    region_stats = []
    
    # Create a mask for each contour and use it to extract pixels for statistics
    for i, contour in enumerate(contours):
        # Create a blank mask
        mask = np.zeros(image.shape, dtype=np.uint8)
        # Fill the contour
        cv2.drawContours(mask, [contour], 0, 255, -1)  # -1 thickness means fill
        
        # Get pixels within the contour
        pixels = image[mask == 255]
        
        if len(pixels) > 0:
            mean_value = np.mean(pixels)
            variance = np.var(pixels)
            area = len(pixels)  # Area in pixels
            
            region_stats.append({
                'region_id': i+1,
                'mean': mean_value,
                'variance': variance,
                'area': area
            })
    
    return region_stats

def process_image_with_overlay(image_path, kernel_radius=5, threshold=30000):
    # Load the image in 16-bit grayscale format
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None or image.dtype != np.uint16:
        print(f"Skipping {image_path}: Not a valid 16-bit grayscale image.")
        return None, None, None

    # Generate an octagon-shaped kernel using skimage
    kernel = octagon(kernel_radius, kernel_radius)
    normalized_kernel = kernel.astype(np.float32) / np.sum(kernel)

    # Apply the octagonal kernel to compute local mean values
    mean_image = cv2.filter2D(image.astype(np.float32), -1, normalized_kernel)

    # Threshold the convolved image to create a binary mask
    mask = (mean_image > threshold).astype(np.uint8)
    mask = mask * 255

    # Find contours of the regions above threshold
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate statistics for regions within contours
    region_stats = calculate_region_statistics(image, contours)
    
    # Create a copy of the original image to overlay boundaries
    overlay_image = cv2.normalize(image.copy(), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(overlay_image, contours, -1, (137, 9, 240), 1)

    return overlay_image, contours, region_stats

def save_statistics_to_file(stats, output_path):
    """Save region statistics to a text file"""
    with open(output_path, 'w') as file:
        file.write("Region Statistics\n")
        file.write("=======================================\n\n")
        
        file.write(f"Total regions detected: {len(stats)}\n\n")
        
        if len(stats) > 0:
            file.write("Region details:\n")
            file.write("---------------------------------------\n")
            
            for region in stats:
                file.write(f"Region {region['region_id']}:\n")
                file.write(f"  Mean value: {region['mean']:.2f}\n")
                file.write(f"  Variance: {region['variance']:.2f}\n")
                file.write(f"  Area (pixels): {region['area']}\n")
                file.write("---------------------------------------\n")
        else:
            file.write("No regions detected above the threshold.\n")

def process_folder(input_folder, output_folder, stats_folder, kernel_radius=5, threshold=30000):
    # Create output folders if they don't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)
        
    # Get all image files with common image extensions
    image_extensions = ['*.png', '*.tif', '*.tiff', '*.jpg', '*.jpeg']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        image_files.extend(glob.glob(os.path.join(input_folder, ext.upper())))
    
    # Process each image
    processed_count = 0
    
    for image_path in image_files:
        file_name = os.path.basename(image_path)
        base_name = os.path.splitext(file_name)[0]
        
        output_path = os.path.join(output_folder, file_name)
        stats_path = os.path.join(stats_folder, f"{base_name}.txt")
        
        print(f"Processing: {image_path}")
        overlay_image, contours, region_stats = process_image_with_overlay(image_path, kernel_radius, threshold)
        
        if overlay_image is not None:
            # Save the overlay image
            cv2.imwrite(output_path, overlay_image)
            
            # Save statistics to text file
            save_statistics_to_file(region_stats, stats_path)
            
            processed_count += 1
            print(f"Saved image: {output_path} (Found {len(contours)} contours)")
            print(f"Saved stats: {stats_path}")
    
    print(f"Processing complete: {processed_count} images processed out of {len(image_files)}")

# Example usage:
input_folder = "Compatible_Input"  # Change this to your folder path
output_folder = "Processed_Images"  # Change this to your desired output folder
stats_folder = "Processed_Stats"  # Folder for statistics text files
process_folder(input_folder, output_folder, stats_folder, kernel_radius=3, threshold=37000)
