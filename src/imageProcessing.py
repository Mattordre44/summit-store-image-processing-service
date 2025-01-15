import io
import numpy as np
from collections import Counter
from PIL import Image
from rembg import remove


def is_background_uniform(image_data, color_tolerance=10, threshold=0.20):
    """
    Checks if the background is uniform by analyzing color variability.
    :param image_data: Image data as bytes
    :param color_tolerance: Color tolerance to group similar colors
    :param threshold: Proportion threshold for the dominant color
    :rtype: bool
    :return: True if the background is uniform, False otherwise
    """
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    img = img.resize((100, 100))  # Resize to speed up analysis
    pixels = np.array(img).reshape(-1, 3)  # Flatten pixels to (N, 3)

    # Round pixel values to reduce noise and group similar colors
    rounded_pixels = [tuple((p // color_tolerance) * color_tolerance) for p in pixels]

    # Count occurrences of each color
    color_counts = Counter(rounded_pixels)
    total_pixels = len(rounded_pixels)

    # Find the most dominant color
    _, count = color_counts.most_common(1)[0]

    # Calculate the proportion of the dominant color
    proportion = count / total_pixels

    # If the dominant color covers at least the threshold (e.g., 80%), return True
    return proportion >= threshold


def remove_background(image_data):
    """
    Remove the background from an image.
    :param image_data: Image data as bytes
    :rtype: bytes
    :return: Processed image data
    """
    return remove(image_data)