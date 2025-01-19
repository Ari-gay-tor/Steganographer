from PIL import Image

def decode_message(image, encoding_type):
    width, height = image.size
    pixels = image.load()
    message = ""
    typ = 0

    if encoding_type == 1:  # Transparency encoding
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if (r, g, b, a) == (0, 0, 0, 0):  # End of message signal
                    return message
                message += chr(a)  # Extract ASCII value from alpha channel
    elif encoding_type == 2:  # Color encoding
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if (r, g, b, a) == (0, 0, 0, 1):  # End of message signal
                    return message
                # Extract the digits from RGB values
                char = (r % 10) + (g % 10) * 10 + (b % 10) * 100
                message += chr(char)
    return message

def main():
    img_path = input("Enter your image file path to decode: ")
    img = Image.open(img_path).convert('RGBA')

    encoding_type = int(input("Enter 1 for transparency encoding and 2 for color encoding: "))
    
    decoded_message = decode_message(img, encoding_type)
    print(f"Decoded message: {decoded_message}")

if __name__ == "__main__":
    main()
