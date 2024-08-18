# start - ncd - 562

import os
import re

# Directory containing the files
data_directory = './output_other'
new_directory = './renamed_output_other'

# Starting numbers for each class
# starting_numbers = {'ncd': 562}
# starting_numbers = {'cocci': 2476}
# starting_numbers = {'healthy': 2404}
starting_numbers = {'salmo': 2625}

# Counters for each class
counters = starting_numbers.copy()

def get_new_filename(class_name, ext):
    # Get the new number for this class
    new_number = counters[class_name]
    
    # Create the new filename
    new_filename = f"{class_name}.{new_number}{ext}"
    return new_filename

# Function to rename the files
def rename_files(data_directory):
    # Loop through all files in the directory
    for filename in os.listdir(data_directory):
        # Only process .jpg files
        if filename.endswith('.jpg'):
            # Use regex to extract class name and extension
            match = re.match(r"^salmo\.\d+_aug_\d+\.jpg$", filename)
            if match:
                class_name = filename.split(".")[0]
                # class_name = match.group(1)
                # Construct the new filenames for both .jpg and .txt
                new_jpg_filename = get_new_filename(class_name, '.jpg')
                new_txt_filename = get_new_filename(class_name, '.txt')

                # Increment the counter for the next file
                counters[class_name] += 1

                # Paths for the old and new .jpg files
                old_jpg_file = os.path.join(data_directory, filename)
                new_jpg_file = os.path.join(new_directory, new_jpg_filename)

                # Paths for the old and new .txt files
                old_txt_file = old_jpg_file.replace('.jpg', '.txt')
                new_txt_file = new_jpg_file.replace('.jpg', '.txt')

                # Rename the .jpg file
                os.rename(old_jpg_file, new_jpg_file)
                # Rename the corresponding .txt file if it exists
                if os.path.exists(old_txt_file):
                    os.rename(old_txt_file, new_txt_file)
                print(f'Renamed: {old_jpg_file} -> {new_jpg_file}')
                print(f'Renamed: {old_txt_file} -> {new_txt_file}')

# Call the function to rename files
rename_files(data_directory)
print("Renaming completed.")