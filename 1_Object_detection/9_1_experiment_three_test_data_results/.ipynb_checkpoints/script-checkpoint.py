import os
import cv2
import glob
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLOv10

# Function to load images and annotations
def load_images_and_annotations(image_dir, annotation_dir):
    images = []
    annotations = []

    image_files = glob.glob(os.path.join(image_dir, '*.jpg'))
    for image_file in image_files:
        image = cv2.imread(image_file)
        images.append(image)

        annotation_file = os.path.join(annotation_dir, os.path.basename(image_file).replace('.jpg', '.txt'))
        with open(annotation_file, 'r') as file:
            bboxes = [line.strip().split() for line in file.readlines()]
            annotations.append(bboxes)

    return images, annotations

# Function to run inference
def run_inference(model, images):
    predictions = []
    for image in images:
        results = model.predict(image)
        predictions.append(results[0])
    return predictions

# Function to calculate metrics and plot confusion matrix
def calculate_metrics(predictions, annotations):
    y_true = []
    y_pred = []

    for pred, ann in zip(predictions, annotations):
        for bbox in ann:
            label = int(bbox[0])
            y_true.append(label)
            matched = False
            for pred_bbox in pred.boxes.cls:
                pred_label = int(pred_bbox)
                if pred_label == label:
                    matched = True
                    y_pred.append(pred_label)
                    break
            if not matched:
                y_pred.append(-1)  # For unmatched ground truth labels

    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=np.unique(y_true))

    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y_true))
    disp.plot(cmap=plt.cm.Blues)
    plt.show()

# Load the model
HOME = os.getcwd()
model = YOLOv10(f'{HOME}/weights/best.pt')

# Load test data
test_image_dir = './datasets/dataset/test/images'
test_annotation_dir = './datasets/dataset/test/labels'
images, annotations = load_images_and_annotations(test_image_dir, test_annotation_dir)

# Run inference
predictions = run_inference(model, images)

# Calculate metrics and plot confusion matrix
calculate_metrics(predictions, annotations)
