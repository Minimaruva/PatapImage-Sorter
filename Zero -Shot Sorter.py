import os
import shutil
import torch
from transformers import pipeline


# Path configuration
INPUT_PATH = os.path.join(os.path.dirname(__file__), "Test Images")
SUCCESS_PATH = os.path.join(os.path.dirname(__file__), "Sorted")
FAILURE_PATH = os.path.join(os.path.dirname(__file__), "Failed")

# Classification configuration
CLASSES = [
    "Pets and Animals", 
    "Family Gatherings", 
    "Vacation Photos",
    "School Events", 
    "Birthdays and Celebrations",
    "Food and Cooking", 
    "Landscapes", 
    "City and Architecture",
    "Selfies and Portraits"
]
MODEL_NAME = "openai/clip-vit-base-patch32"  # OpenAI CLIP model
BATCH_SIZE = 16


def setup_folders():
    """Create necessary folder structure if it doesn't exist"""
    for path in [SUCCESS_PATH, FAILURE_PATH]:
        if not os.path.exists(path):
            os.makedirs(path)


def get_image_paths(dir_path):
    """Collect all image paths from the input directory"""
    image_paths = [
        entry.path
        for entry in os.scandir(dir_path)
        if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    
    if not image_paths:
        print(f"No images found in {dir_path}. Exiting.")
    
    return image_paths


def load_classifier(model_name=MODEL_NAME):
    """Initialize and load the zero-shot classifier"""
    device = 0 if torch.cuda.is_available() else -1
    classifier = pipeline(
        "zero-shot-image-classification",
        model=model_name,
        device=device,
        use_fast=True
    )
    return classifier, device


def classify_images(classifier, image_paths, classes=CLASSES, batch_size=BATCH_SIZE):
    """Classify images in batches"""
    results = []
    
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        batch_results = classifier(
            batch_paths,
            candidate_labels=classes
        )
        results.extend(batch_results)
    
    return results


def sort_images(image_paths, classification_results, confidence_threshold=0.6):
    """Sort images into folders based on classification results with confidence threshold"""
    sorted_count = 0
    unsure_count = 0
    
    for img_path, res in zip(image_paths, classification_results):
        top_score = res[0]["score"]
        top_label = res[0]["label"]
        
        if top_score >= confidence_threshold:
            # High confidence classification
            dest_dir = os.path.join(SUCCESS_PATH, top_label)
            sorted_count += 1
        else:
            # Low confidence - mark as unsure
            dest_dir = os.path.join(SUCCESS_PATH, "Unsure")
            unsure_count += 1
            
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        shutil.copy2(img_path, os.path.join(dest_dir, os.path.basename(img_path)))
    
    print(f"Sorted {sorted_count} images with high confidence")
    print(f"Moved {unsure_count} images to 'Unsure' category")


def main(classes=CLASSES, model_name=MODEL_NAME, batch_size=BATCH_SIZE):
    # Setup necessary folders
    setup_folders()
    
    # Get image paths
    image_paths = get_image_paths(INPUT_PATH)
    if not image_paths:
        return
    
    # Load classifier and detect device
    classifier, device = load_classifier(model_name)
    
    # Classify all images
    results = classify_images(classifier, image_paths, classes, batch_size)
    
    # Sort images based on results
    sort_images(image_paths, results)


if __name__ == "__main__":
    main()