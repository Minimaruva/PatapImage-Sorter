import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS


SUCCESS_PATH = os.path.join(os.path.dirname(__file__), 'Sorted')
FAILURE_PATH = os.path.join(os.path.dirname(__file__), 'Failed')

# Setup folder structure
if not os.path.exists(SUCCESS_PATH):
    os.makedirs(SUCCESS_PATH)
if not os.path.exists(FAILURE_PATH):
    os.makedirs(FAILURE_PATH)


def get_image_date(image_path):
    date_found = None
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':  # Look for the date tag
                        date_found = value
                        break
    except Image.UnidentifiedImageError:
        print(f"Error: {image_path} is not a valid image file.")
    except Exception as e:
        print(f"Error: {e} while processing {image_path}.")
    finally:
        return date_found


def categorise(dir_path):
    images_info = {}
    for entry in os.scandir(dir_path):
        if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = entry.path
            date = get_image_date(image_path)
            if date:
                # Extract year and month directly from the EXIF date format 'YYYY:MM:DD HH:MM:SS'
                date_parts = date.split(' ')[0].split(':')
                if len(date_parts) >= 2:
                    year = date_parts[0]    # Extract year (e.g., '2023')
                    month = date_parts[1]   # Extract month (e.g., '01', '05', '12')
                    
                    # Create directories: /Sorted/YYYY/MM/
                    new_dir = os.path.join(SUCCESS_PATH, year, month)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                        
                    # Set destination path for the image
                    new_path = os.path.join(new_dir, entry.name)
                    images_info[image_path] = new_path
                else:
                    print(f"Warning: Could not extract year and month from {image_path}: {date}")
                    images_info[image_path] = os.path.join(FAILURE_PATH, entry.name)
            else:
                images_info[image_path] = os.path.join(FAILURE_PATH, entry.name)
            
            # Copy the file instead of moving it
            if image_path in images_info:
                shutil.copy2(image_path, images_info[image_path])
            else:
                print(f"Error: No destination path determined for {image_path}. Skipping copy.")


categorise(os.path.join(os.path.dirname(__file__), 'Test Images'))
# get_image_date("./python.txt")
