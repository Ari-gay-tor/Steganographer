from PIL import Image
import os
def decode_transparency(image):
    width, height = image.size
    pixels = image.load()
    message = ""
    typ = 0

    # Start decoding from the second pixel onwards
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (r, g, b, a) == (0, 0, 0, 0):  # End of message signal
                return message
            message += chr(a)  # Extract ASCII value from alpha channel
    return message

def decode_color(image):
    width, height = image.size
    pixels = image.load()
    message = ""
    typ = 0

    # Start decoding from the second pixel onwards
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (r, g, b, a) == (0, 0, 0, 1):  # End of message signal
                return message

            # Decode the message by extracting digits from RGB values
            char = (r % 10) + (g % 10) * 10 + (b % 10) * 100
            message += chr(char)
    return message

def main():
    img_path = input("Enter your image file path to decode: ")
    img = Image.open(img_path).convert('RGBA')

    # Check the first pixel to determine encoding type
    first_pixel = img.getpixel((0, 0))
    print(first_pixel)
    if first_pixel == (0, 0, 0, 0):  # Transparency encoding
        print("Detected transparency encoding.")
        decoded_message = decode_transparency(img)
    elif first_pixel == (0, 0, 0, 1):  # Color encoding
        print("Detected color encoding.")
        decoded_message = decode_color(img)
    else:
        print("Error: Invalid first pixel value, unable to determine encoding.")
        return
    
    print(f"Decoded message: {decoded_message}")
    if os.path.exists(img_path):
        os.remove(img_path)
if __name__ == "__main__":
    main()
