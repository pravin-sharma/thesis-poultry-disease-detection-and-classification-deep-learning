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

# Define augmentation pipeline without ToTensorV2
augmentation = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(p=0.5, shift_limit=0.1, scale_limit=0.1, rotate_limit=45),
    A.RandomBrightnessContrast(p=0.5),
    A.RandomSizedBBoxSafeCrop(height=640, width=640, p=0.5)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['labels']))

def clip_bboxes(bboxes, img_width, img_height):
    clipped_bboxes = []
    for bbox in bboxes:
        xmin, ymin, xmax, ymax = bbox
        xmin = max(0, min(xmin, img_width - 1))
        ymin = max(0, min(ymin, img_height - 1))
        xmax = max(0, min(xmax, img_width - 1))
        ymax = max(0, min(ymax, img_height - 1))
        clipped_bboxes.append([xmin, ymin, xmax, ymax])
    return clipped_bboxes

def augment_image(image, pascal_bboxes, labels):
    augmented = augmentation(image=image, bboxes=pascal_bboxes, labels=labels)
    clipped_bboxes = clip_bboxes(augmented['bboxes'], image.shape[1], image.shape[0])
    return augmented['image'], clipped_bboxes, augmented['labels']

def process_image(image_path, annotation_path, output_dir, num_augmentations=5):
    # Read image
    image = cv2.imread(image_path)
    img_height, img_width = image.shape[:2]

    # Read YOLO annotations
    pascal_bboxes, labels = read_yolo_annotations(annotation_path, img_width, img_height)
    
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    
    for i in range(num_augmentations):
        # Apply augmentation
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

def process_folder(input_folder, output_folder, num_augmentations=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.startswith('ncd') and (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):
            image_path = os.path.join(input_folder, filename)
            annotation_path = os.path.join(input_folder, os.path.splitext(filename)[0] + '.txt')
            
            if os.path.exists(annotation_path):
                process_image(image_path, annotation_path, output_folder, num_augmentations)

# Example usage
input_folder = '../../dataset/8_resized_640'
output_folder = './output_ncd'

process_folder(input_folder, output_folder, num_augmentations=4)
