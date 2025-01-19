from PIL import Image
import os

# Input image path
img_path = input("Enter your image path: ")

# Open the encoded image
img = Image.open(img_path)
width, height = img.size
pixels = img.load()

# First character of the path is used to determine encoding scheme
c = img_path[0]
decoded_message = ""
# Iterate over the pixels to decode the message
for y in range(height):
    for x in range(width):
        # Get the current pixel's RGBA values
        r, g, b, a = pixels[x, y]
            
        # Extract the ASCII value from the alpha channel (a)
        ascii_val = a  # Directly use the alpha value as the ASCII code

        # Convert ASCII value to character
        char = chr(ascii_val)

        # Check for the termination character '&'
        if char == '&':
            break

        # Append the character to the decoded message
        decoded_message += char

    # Exit the outer loop if the termination character is found
    if char == '&':
        break

# Print the decoded message
print(f"Decoded message: {decoded_message}")

if os.path.exists(img_path):
    os.remove(img_path)