from color_finder import ColorFinder, SimpleRemovalStrategy

# Path to your image
image_path = 'red.jpg'

# Initialize the ColorFinder with a simple background removal strategy
color_finder = ColorFinder(image_path, color_dict, SimpleRemovalStrategy(threshold=240))

# Process the image to find the closest named color
closest_color = color_finder.process_image()
print(f"The closest color name is {closest_color}.")