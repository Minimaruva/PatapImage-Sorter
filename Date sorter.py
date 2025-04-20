import os
from PIL import Image
from PIL.ExifTags import TAGS


SUCCESS_PATH = os.path.join(os.path.dirname(__file__), 'Sorted')
FAILURE_PATH = os.path.join(os.path.dirname(__file__), 'Failed')

# Setup folder sturcture
if not os.path.exists(SUCCESS_PATH):
    os.makedirs(SUCCESS_PATH)
if not os.path.exists(FAILURE_PATH):
    os.makedirs(FAILURE_PATH)


def categorise(dir_path):
    images_info = {}
    with Image.open(dir_path+"/Catapilla.jpg") as img:
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':  # Look for the date tag
                    return value

    

# directory_path = input("Enter the directory path (default is ./Test Images): ")

# if not directory_path:
#     directory_path = os.path.join(os.path.dirname(__file__), 'Test Images')
#     print(categorise(directory_path))

print(categorise(os.path.join(os.path.dirname(__file__), 'Test Images')))