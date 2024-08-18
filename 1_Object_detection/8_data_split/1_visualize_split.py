import os

# Directory containing the images and labels
directory = './9_balanced_dataset'

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