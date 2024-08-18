import os
from collections import defaultdict

def count_images_from_filenames(directory):
    # Dictionary to hold counts of images per class
    counts = defaultdict(int)
    
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    for file in files:
        # Extract class label from filename
        # Assuming the class label is the first part of the filename before an underscore
        class_label = file.split('.')[0]
        counts[class_label] += 1
    
    return counts

def print_counts(counts):
    print("Image counts per class:")
    for class_name, count in counts.items():
        print(f"  {class_name}: {count} images")

# Define the directory containing all images
directory = './datasets/dataset/test/images'  # Change this to your actual directory path

# Count images
image_counts = count_images_from_filenames(directory)

# Print results
print_counts(image_counts)
