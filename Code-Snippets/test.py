from PIL import Image
import os
img_path=input("Enter your image path: ")
img_path = img_path.strip('"')
# Open the encoded image
img = Image.open(img_path)
width, height = img.size
pixels = img.load()
decoded_message = ""
textfile = open("Output.txt", "w")
if pixels[0,0] == (0,0,0,0):
    print("Detected transparency encoding.")
    # Iterate over the pixels to decode the message
    for y in range (height):
        for x in range (width):
            # Get the current pixel's RGBA values
            r, g, b, a = pixels[x, y]
            # Extract the transperency value from RGBA format
            ascii_val = a
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
    textfile.write(decoded_message)

if pixels[0,0] == (0,0,0,1):
    print("Detected colour encoding.")
    # Iterate over the pixels to decode the message
    for y in range(height):
        for x in range(width):
            # Get the current pixel's RGBA values
            r, g, b, a = pixels[x, y]

            # Extract the ASCII value from the least significant digits of RGB
            ascii_val = (r % 10) + (g % 10) * 10 + (b % 10) * 100

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
    textfile.write(decoded_message)
if os.path.exists(img_path):
    os.remove(img_path)
