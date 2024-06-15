import cv2
import numpy as np

def add_outline(image_path, output_path, outline_type='solid', thickness=1, gap=10, color=(0, 0, 255, 255), distance=10):
    """
    Add an outline to an object in a PNG image.

    Parameters:
    - image_path: str, path to the input image.
    - output_path: str, path to save the output image.
    - outline_type: str, 'solid', 'dotted', or 'dashed' to specify the type of outline.
    - thickness: int, thickness of the outline.
    - gap: int, gap between dots or dashes.
    - color: tuple, color of the outline in (B, G, R, A) format.
    - distance: int, distance between the object and the outline.
    """
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a binary mask of the object
    _, binary_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Dilate the mask to create space between the object and the outline
    dilated_mask = cv2.dilate(binary_mask, np.ones((distance, distance), np.uint8))  # Adjust the kernel size for more space

    # Detect edges on the dilated mask
    edges = cv2.Canny(dilated_mask, 100, 200)

    # Find contours from the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Create an outline mask
    outline_mask = np.zeros_like(image)

    if outline_type == 'solid':
        # Draw solid outline
        cv2.drawContours(outline_mask, contours, -1, color, thickness)
    elif outline_type == 'dotted':
        # Draw dotted outline
        for contour in contours:
            for i in range(0, len(contour), gap):
                cv2.circle(outline_mask, tuple(contour[i][0]), thickness, color, -1)
    elif outline_type == 'dashed':
        # Draw dashed outline
        dash_length = gap  # Length of each dash
        for contour in contours:
            for i in range(0, len(contour), 2 * dash_length):
                start_idx = i
                end_idx = min(i + dash_length, len(contour) - 1)
                cv2.line(outline_mask, tuple(contour[start_idx][0]), tuple(contour[end_idx][0]), color, thickness)

    # Combine the original image with the outline
    outlined_image = cv2.addWeighted(image, 1, outline_mask, 1, 0)

    # Save the result
    cv2.imwrite(output_path, outlined_image)
