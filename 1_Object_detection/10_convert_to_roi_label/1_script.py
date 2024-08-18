# dir = 'C:\Users\pravi\OneDrive\Desktop\Pravin\Study\Masters\Research_Project\dataset\1_Object_detection\11_balanced_data_split_roi_label\dataset'

import os

# Set the path to the main directory containing the three folders
main_dir = "../../../dataset/1_Object_detection/11_balanced_data_split_roi_label/dataset"

# Traverse each folder inside the main directory
for folder_name in os.listdir(main_dir):
    folder_path = os.path.join(main_dir, folder_name)
    
    # Ensure it's a directory and contains a 'labels' folder
    if os.path.isdir(folder_path):
        labels_folder = os.path.join(folder_path, 'labels')
        
        if os.path.exists(labels_folder) and os.path.isdir(labels_folder):
            # Iterate through each text file in the labels folder
            for filename in os.listdir(labels_folder):
                file_path = os.path.join(labels_folder, filename)
                
                if filename.endswith('.txt'):
                    # Read the contents of the file
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                    
                    # Replace the first value of each line with '0'
                    updated_lines = []
                    for line in lines:
                        parts = line.split()
                        parts[0] = '0'
                        updated_lines.append(' '.join(parts) + '\n')
                    
                    # Write the updated lines back to the file
                    with open(file_path, 'w') as file:
                        file.writelines(updated_lines)

print("All files updated successfully!")
