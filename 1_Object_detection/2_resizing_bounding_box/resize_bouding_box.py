import os
import cv2

def resize_image_and_bboxes(image_path, annotation_path, output_image_path, output_annotation_path, new_width, new_height):
    # Load image
    image = cv2.imread(image_path)
    original_height, original_width = image.shape[:2]
    
    # Read YOLO annotations
    with open(annotation_path, 'r') as file:
        lines = file.readlines()
    
    # Resize image
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Calculate scale factors
    x_scale = new_width / original_width
    y_scale = new_height / original_height
    
    # Adjust bounding boxes
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1]) * original_width
        y_center = float(parts[2]) * original_height
        width = float(parts[3]) * original_width
        height = float(parts[4]) * original_height
        
        # Scale bounding box
        x_center = x_center * x_scale
        y_center = y_center * y_scale
        width = width * x_scale
        height = height * y_scale
        
        # Normalize bounding box
        x_center /= new_width
        y_center /= new_height
        width /= new_width
        height /= new_height
        
        new_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        new_lines.append(new_line)
    
    # Save resized image
    cv2.imwrite(output_image_path, resized_image)
    
    # Save updated annotations
    with open(output_annotation_path, 'w') as file:
        file.writelines(new_lines)

def process_folder(input_image_folder, input_annotation_folder, output_image_folder, output_annotation_folder, new_width, new_height):
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    
    if not os.path.exists(output_annotation_folder):
        os.makedirs(output_annotation_folder)
    
    image_files = [f for f in os.listdir(input_image_folder) if f.endswith('.jpg') or f.endswith('.png')]

    for image_file in image_files:
        image_path = os.path.join(input_image_folder, image_file)
        annotation_path = os.path.join(input_annotation_folder, os.path.splitext(image_file)[0] + '.txt')
        output_image_path = os.path.join(output_image_folder, image_file)
        output_annotation_path = os.path.join(output_annotation_folder, os.path.splitext(image_file)[0] + '.txt')

        if os.path.exists(annotation_path):
            resize_image_and_bboxes(image_path, annotation_path, output_image_path, output_annotation_path, new_width, new_height)
        else:
            print(f"Warning: Annotation file not found for {image_file}")

# Example usage
input_image_folder = './data/test/images'
input_annotation_folder = './data/test/labels'
output_image_folder = './resized/test/images'
output_annotation_folder = './resized/test/labels'
new_width = 640
new_height = 640
process_folder(input_image_folder, input_annotation_folder, output_image_folder, output_annotation_folder, new_width, new_height)
