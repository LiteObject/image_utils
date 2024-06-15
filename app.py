import image_utils

# Example usage
image_utils.add_outline(
    image_path='images/PP.png', 
    output_path='images/outlined_image_1.png',
    outline_type='dotted', 
    thickness=3, 
    gap=20, 
    color=(0, 255, 0, 255), 
    distance=20)
