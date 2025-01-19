from PIL import Image

# Open the encoded image
img = Image.open("Output.png")
width, height = img.size
pixels = img.load()

decoded_message = ""

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
