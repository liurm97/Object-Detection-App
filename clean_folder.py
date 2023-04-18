import glob
import os

PATH = "images/*.png"
def clean_folder():
    """Cleans up images folder"""
    images = glob.glob(PATH)
    [os.remove(image) for image in images]
    return

if __name__ == "__main__":
    clean_folder()