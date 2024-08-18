# ==============================================================================
## rename pcr images 
# ==============================================================================
## all the file in the dir whose name starts with pcr eg: prccocci.0.jpg,prccocci.0.txt,prchealthy.0.jpg,...
## rename them to cocci.0.jpg,....
# import os

# def rename_files(directory):
#     for filename in os.listdir(directory):
#         # Check if the filename starts with "pcr"
#         if filename.startswith("pcr"):
#             # Create the new filename by removing "pcr" prefix
#             new_filename = filename.replace("pcr", "", 1)
#             # Construct the full file paths
#             old_file = os.path.join(directory, filename)
#             new_file = os.path.join(directory, new_filename)
#             # Rename the file
#             os.rename(old_file, new_file)
#             print(f'Renamed: {old_file} -> {new_file}')

# directory = './datasets/pcr_labelled'
# rename_files(directory)
# =================================================================================
# # renumber pcr images
# =================================================================================
# # cocci - 2102
# # healthy - 2056
# # ncd - 375
# # salmo - 2275
# # plus 1 to the above numbers
# import os
# import re

# # Directory containing the files
# directory = './datasets/pcr_labelled'

# # Starting numbers for each class
# starting_numbers = {
#     'cocci': 2103,
#     'healthy': 2057,
#     'ncd': 376,
#     'salmo': 2276
# }

# # Counters for each class
# counters = starting_numbers.copy()

# def get_new_filename(class_name, ext):
#     # Get the new number for this class
#     new_number = counters[class_name]
    
#     # Create the new filename
#     new_filename = f"{class_name}.{new_number}{ext}"
#     return new_filename

# # Function to rename the files
# def rename_files(directory):
#     # Loop through all files in the directory
#     for filename in os.listdir(directory):
#         # Only process .jpg files
#         if filename.endswith('.jpg'):
#             # Use regex to extract class name and extension
#             match = re.match(r"^(cocci|healthy|ncd|salmo)\.\d+\.jpg$", filename)
#             if match:
#                 class_name = match.group(1)
#                 # Construct the new filenames for both .jpg and .txt
#                 new_jpg_filename = get_new_filename(class_name, '.jpg')
#                 new_txt_filename = get_new_filename(class_name, '.txt')

#                 # Increment the counter for the next file
#                 counters[class_name] += 1

#                 # Paths for the old and new .jpg files
#                 old_jpg_file = os.path.join(directory, filename)
#                 new_jpg_file = os.path.join(directory, new_jpg_filename)

#                 # Paths for the old and new .txt files
#                 old_txt_file = old_jpg_file.replace('.jpg', '.txt')
#                 new_txt_file = new_jpg_file.replace('.jpg', '.txt')

#                 # Rename the .jpg file
#                 os.rename(old_jpg_file, new_jpg_file)
#                 # Rename the corresponding .txt file if it exists
#                 if os.path.exists(old_txt_file):
#                     os.rename(old_txt_file, new_txt_file)
#                 print(f'Renamed: {old_jpg_file} -> {new_jpg_file}')
#                 print(f'Renamed: {old_txt_file} -> {new_txt_file}')

# # Call the function to rename files
# rename_files(directory)
# print("Renaming completed.")
# =====================================================================================
## merge images - manual merge after renaming, in a single folder
# ======================================================================================
# # Resize Image

# import os
# import cv2

# def resize_image_and_bboxes(image_path, annotation_path, output_image_path, output_annotation_path, new_width, new_height):
#     # Load image
#     image = cv2.imread(image_path)
#     original_height, original_width = image.shape[:2]
    
#     # Read YOLO annotations
#     with open(annotation_path, 'r') as file:
#         lines = file.readlines()
    
#     # Resize image
#     resized_image = cv2.resize(image, (new_width, new_height))
    
#     # Calculate scale factors
#     x_scale = new_width / original_width
#     y_scale = new_height / original_height
    
#     # Adjust bounding boxes
#     new_lines = []
#     for line in lines:
#         parts = line.strip().split()
#         class_id = int(parts[0])
#         x_center = float(parts[1]) * original_width
#         y_center = float(parts[2]) * original_height
#         width = float(parts[3]) * original_width
#         height = float(parts[4]) * original_height
        
#         # Scale bounding box
#         x_center = x_center * x_scale
#         y_center = y_center * y_scale
#         width = width * x_scale
#         height = height * y_scale
        
#         # Normalize bounding box
#         x_center /= new_width
#         y_center /= new_height
#         width /= new_width
#         height /= new_height
        
#         new_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
#         new_lines.append(new_line)
    
#     # Save resized image
#     cv2.imwrite(output_image_path, resized_image)
    
#     # Save updated annotations
#     with open(output_annotation_path, 'w') as file:
#         file.writelines(new_lines)

# def process_folder(input_image_folder, input_annotation_folder, output_image_folder, output_annotation_folder, new_width, new_height):
#     if not os.path.exists(output_image_folder):
#         os.makedirs(output_image_folder)
    
#     if not os.path.exists(output_annotation_folder):
#         os.makedirs(output_annotation_folder)
    
#     image_files = [f for f in os.listdir(input_image_folder) if f.endswith('.jpg') or f.endswith('.png')]

#     for image_file in image_files:
#         image_path = os.path.join(input_image_folder, image_file)
#         annotation_path = os.path.join(input_annotation_folder, os.path.splitext(image_file)[0] + '.txt')
#         output_image_path = os.path.join(output_image_folder, image_file)
#         output_annotation_path = os.path.join(output_annotation_folder, os.path.splitext(image_file)[0] + '.txt')

#         if os.path.exists(annotation_path):
#             resize_image_and_bboxes(image_path, annotation_path, output_image_path, output_annotation_path, new_width, new_height)
#         else:
#             print(f"Warning: Annotation file not found for {image_file}")

# # Example usage
# input_image_folder = './datasets'
# input_annotation_folder = './datasets'
# output_image_folder = './resized'
# output_annotation_folder = './resized'
# new_width = 640
# new_height = 640
# process_folder(input_image_folder, input_annotation_folder, output_image_folder, output_annotation_folder, new_width, new_height)

## Visualize number of images in each class
import os

# Directory containing the images and labels
directory = './resized'

# Dictionary to store the counts of each class
class_counts = {}

# Function to count the images for each class
def count_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            # Extract the class name from the filename (assuming filename format: class.number.jpg)
            class_name = filename.split('.')[0]
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

# Count the images
count_images(directory)

# Print the counts for each class
for class_name, count in class_counts.items():
    print(f"Class '{class_name}': {count} images")
 


