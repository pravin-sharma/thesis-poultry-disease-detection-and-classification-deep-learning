import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
src_dir = os.path.join(os.getcwd(), '9_balanced_dataset')
all_images_dir = os.path.join(src_dir, 'all_images')
all_labels_dir = os.path.join(src_dir, 'all_labels')

target_dirs = ['train', 'test', 'valid']
ratios = {'train': 0.7, 'test': 0.2, 'valid': 0.1}
seed = 4224  # Fixed seed for reproducibility

# Create directories
for dir_name in target_dirs:
    dir_path = os.path.join(src_dir, dir_name)
    images_path = os.path.join(dir_path, 'images')
    labels_path = os.path.join(dir_path, 'labels')
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(labels_path, exist_ok=True)

# Get file lists and their labels
images = [f for f in os.listdir(all_images_dir) if f.endswith('.jpg')]
labels = [f.replace('.jpg', '.txt') for f in images]

# Extract class information from labels (assuming labels contain class info in the filename or content)
# Here we assume class info is in the filename before the first dot (e.g., 'class1.xxx.jpg')
def get_class(filename):
    return filename.split('.')[0]

classes = [get_class(img) for img in images]

# Perform stratified split
train_imgs, temp_imgs, train_classes, temp_classes = train_test_split(images, classes, stratify=classes, test_size=1-ratios['train'], random_state=seed)
test_ratio_adjusted = ratios['test'] / (ratios['test'] + ratios['valid'])
valid_imgs, test_imgs, valid_classes, test_classes = train_test_split(temp_imgs, temp_classes, stratify=temp_classes, test_size=test_ratio_adjusted, random_state=seed)

splits = {
    'train': train_imgs,
    'test': test_imgs,
    'valid': valid_imgs
}

# Move files
def move_files(files, dest):
    for file in files:
        image_src_path = os.path.join(all_images_dir, file)
        label_src_path = os.path.join(all_labels_dir, file.replace('.jpg', '.txt'))
        image_dest_path = os.path.join(src_dir, dest, 'images', file)
        label_dest_path = os.path.join(src_dir, dest, 'labels', file.replace('.jpg', '.txt'))

        if os.path.exists(image_src_path):
            shutil.move(image_src_path, image_dest_path)
        if os.path.exists(label_src_path):
            shutil.move(label_src_path, label_dest_path)

for key in splits:
    move_files(splits[key], key)

print('Data stratified split and moved successfully.')
