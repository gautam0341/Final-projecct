import requests


def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    url = f'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={apod_date}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    if apod_info_dict['media_type'] == 'image':
        return apod_info_dict['hdurl']
    elif apod_info_dict['media_type'] == 'video':
        return apod_info_dict['thumbnail_url']
    else:
        return None


def main():
    # Example usage:
    apod_date = '2020-02-05'
    apod_info = get_apod_info(apod_date)
    if apod_info is not None:
        print(get_apod_image_url(apod_info))
    else:
        print(f'Failed to get APOD info for {apod_date}')


if __name__ == '__main__':
    main()
