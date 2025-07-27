# from picamera2 import Picamera2
import os
import subprocess
import base64
import requests 

from .config import (
    CAMERA_MODE
)

CORE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CORE_DIR, ".."))
PHOTO_HISTORY_DIR = os.path.join(PROJECT_ROOT, "photos")

os.makedirs(PHOTO_HISTORY_DIR, exist_ok=True)


# def __init__(self):
#     # Initialize the camera
#     self.picam2 = Picamera2()
#     # Configure the camera
#     self.config = picam2.create_still_configuration(lores={"size": (640, 480)}, display="lores")
#     self.picam2.configure(self.config)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def rotate_image_files():
    # Rotate old files first (2 -> 3, 1 -> 2)
    for i in range(2, 0, -1):
        src = os.path.join(PHOTO_HISTORY_DIR, f"photo-{i}.jpg")
        dst = os.path.join(PHOTO_HISTORY_DIR, f"photo-{i + 1}.jpg")
        if os.path.exists(src):
            os.replace(src, dst)

def take_photo(name="photo-1.jpg"):

    """ Capture a photo using the Picamera2 library and save it as 'photo.jpg'. """

    if CAMERA_MODE != "normal":
        print("Camera mode is not set to 'normal'. Skipping photo capture.")
        return None

    # Log the action
    print("Taking a photo...")

    if name == "photo-1.jpg":
        rotate_image_files()

    full_path = os.path.join(PHOTO_HISTORY_DIR, name)

    # cmd = f"rpicam-jpeg -o {full_path} -t 1 -n"

    try:
        # Call the command to capture the photo
        result = subprocess.check_output(
            ["rpicam-jpeg", "-o", full_path, "-n", "-t", "1"],
            cwd=PHOTO_HISTORY_DIR,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()

    except subprocess.CalledProcessError:
        # Failed to capture the photo
        print("[take_photo] Failed to capture photo.")
        return "failed"
        
    if "Still capture image received" in result:
        return "failed"
    
    print("Photo saved ")
    return encode_image(full_path)

    # # Start the camera
    # self.picam2.start(show_preview=False)
    # # Capture the photo
    # self.picam2.capture_file("photo-1.jpg")
    # # Stop the camera
    # self.picam2.stop()



