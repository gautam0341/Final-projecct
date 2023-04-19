'''
Library of useful functions for working with images.
'''
import requests
import ctypes
import os
def main():
    # TODO: Add code to test the functions in this module
    return


def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if successful. None, if unsuccessful.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception if the response status is not 200 OK
        return response.content
    except requests.exceptions.RequestException:
        return None


def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.

    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if successful. False, if unsuccessful
    """
    try:
        with open(image_path, 'wb') as f:
            f.write(image_data)
        return True
    except:
        return False


def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bool: True, if successful. False, if unsuccessful        
    """
    # Verify that the image file exists
    if not os.path.isfile(image_path):
        return False

    # Determine the appropriate SPI_SETDESKWALLPAPER flag based on the operating system
    if os.name == 'nt':
        set_wallpaper = ctypes.windll.user32.SystemParametersInfoW
        flag = 20  # SPI_SETDESKWALLPAPER
    else:
        set_wallpaper = None
        flag = None

    # Set the desktop background image
    if set_wallpaper is not None:
        # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        result = set_wallpaper(flag, 0, image_path, 3)
        return result != 0
    else:
        return False


def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()