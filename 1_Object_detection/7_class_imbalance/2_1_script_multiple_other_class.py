import albumentations as A
import cv2
import numpy as np
import os

def yolo_to_pascal_voc(bbox, img_width, img_height):
    x_center, y_center, width, height = bbox
    xmin = (x_center - width / 2) * img_width
    xmax = (x_center + width / 2) * img_width
    ymin = (y_center - height / 2) * img_height
    ymax = (y_center + height / 2) * img_height
    return [xmin, ymin, xmax, ymax]

def pascal_voc_to_yolo(bbox, img_width, img_height):
    xmin, ymin, xmax, ymax = bbox
    x_center = (xmin + xmax) / 2 / img_width
    y_center = (ymin + ymax) / 2 / img_height
    width = (xmax - xmin) / img_width
    height = (ymax - ymin) / img_height
    return [x_center, y_center, width, height]

def read_yolo_annotations(txt_file, img_width, img_height):
    bboxes = []
    labels = []
    with open(txt_file, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split()
            label = int(parts[0])
            bbox = [float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])]
            pascal_bbox = yolo_to_pascal_voc(bbox, img_width, img_height)
            bboxes.append(pascal_bbox)
            labels.append(label)
    return bboxes, labels

def write_yolo_annotations(txt_file, bboxes, labels, img_width, img_height):
    with open(txt_file, 'w') as file:
        for bbox, label in zip(bboxes, labels):
            yolo_bbox = pascal_voc_to_yolo(bbox, img_width, img_height)
            file.write(f"{label} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}\n")

# Define augmentation pipeline
augmentation = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(p=0.5, shift_limit=0.1, scale_limit=0.1, rotate_limit=45),
    A.RandomBrightnessContrast(p=0.5),
    A.RandomSizedBBoxSafeCrop(height=640, width=640, p=0.5)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['labels']))

def augment_image(image, pascal_bboxes, labels):
    augmented = augmentation(image=image, bboxes=pascal_bboxes, labels=labels)
    return augmented['image'], augmented['bboxes'], augmented['labels']

def augment_images(class_name, current_count, target_count, source_dir, output_dir, augmentations_per_image=3):
    # Get list of images for the class
    images = [f for f in os.listdir(source_dir) if (f.startswith(class_name) and f.endswith('.jpg'))]
    bboxes_dir = source_dir  # Assuming bounding boxes are in the same directory

    img_index = 0
    while current_count < target_count and img_index < len(images):
        img_file = images[img_index]
        image_path = os.path.join(source_dir, img_file)
        annotation_path = os.path.join(bboxes_dir, os.path.splitext(img_file)[0] + '.txt')

        # Read image
        image = cv2.imread(image_path)
        img_height, img_width = image.shape[:2]

        # Read YOLO annotations
        pascal_bboxes, labels = read_yolo_annotations(annotation_path, img_width, img_height)
        
        base_filename = os.path.splitext(os.path.basename(image_path))[0]

        # Apply augmentation
        for i in range(augmentations_per_image):
            if current_count >= target_count:
                break
            augmented_image, augmented_pascal_bboxes, augmented_labels = augment_image(image, pascal_bboxes, labels)
            
            # Convert tensor to numpy array if necessary
            if isinstance(augmented_image, np.ndarray):
                augmented_image_np = augmented_image
            else:
                augmented_image_np = augmented_image.cpu().numpy().transpose(1, 2, 0)
                augmented_image_np = (augmented_image_np * 255).astype(np.uint8)
            
            # Define output paths
            output_image_path = os.path.join(output_dir, f"{base_filename}_aug_{i}.jpg")
            output_annotation_path = os.path.join(output_dir, f"{base_filename}_aug_{i}.txt")
            
            # Write augmented image
            cv2.imwrite(output_image_path, augmented_image_np)
            
            # Write augmented YOLO annotations
            write_yolo_annotations(output_annotation_path, augmented_pascal_bboxes, augmented_labels, img_width, img_height)

            current_count += 1
        
        img_index += 1

# Example usage
source_dir = '../../dataset/8_resized_640'
output_dir = './output_other'

# Target count is the count of 'ncd' images after augmentation
target_count = 2810

# Augment other classes to reach target count
augment_images('cocci', 2476, target_count, source_dir, output_dir)
augment_images('healthy', 2404, target_count, source_dir, output_dir)
augment_images('salmo', 2625, target_count, source_dir, output_dir)
