from PIL import Image

def get_image():
    """
    get_image()
    Asks user for a file path, trims the quotes off the path string and opens the image and converts it to RGBA format.
    """
    img_path = input("Enter your image file path: ").strip('"')
    img = Image.open(img_path)  #Image.open doesn't work for paths like ("C:\Users:\etc"), only works if there are no quotes (C:\Users\etc)
    img = img.convert('RGBA')
    return img

def get_message():
    """
    get_message()
    Prompts the user to enter a message as a string or from a file.
    Returns the message preappended by a space (" ") and postappended with a ("$")
    eg: Original message = "Hello World"
        Returned message = " Hello World$"
    """
    choice = int(input("Enter 1 for string and 2 for file path: "))
    if choice == 1:
        msg = input("Enter string: ")
    elif choice == 2:
        file_path = input("Enter your text file path: ").strip('"')
        with open(file_path, "r") as f:
            msg = f.read()
    else:
        raise ValueError("Invalid choice")
    return " " + msg + "&"

def transparency_encoding(img, ascii_vals):
    """
    transparency_encoding(image, ascii_vals)
    Encodes the ASCII values into the transparency (alpha) channel
    The ascii value gets encoded into the alpha channel of the image
    eg: ASCII = 165
        (R,G,B,A) = (256,256,256,256)
     new(R,G,B,A) = (256,256,256,165) {A gets replaced with the ASCII value}
    """
    pixels = img.load()
    width, height = img.size
    typ = 0

    for y in range(height):
        if typ >= len(ascii_vals):
            break
        for x in range(width):
            if typ >= len(ascii_vals):
                break
            r, g, b, a = pixels[x, y]
            pixels[x, y] = (r, g, b, ascii_vals[typ])
            typ += 1

    pixels[0, 0] = (0, 0, 0, 0)  # Indicator for transparency encoding

def color_encoding(img, ascii_vals):
    """
    color_encoding(image, ascii_vals)
    Encodes the ASCII values into the color channels (RGB)
    First digit of ASCII goes into the last digit of the red channel, second digit goes into the last digit of green channel and last digit goes into the last digit of the blue channel
    eg: ASCII = 165
        (R,G,B) = (100,100,100)
     new(R,G,B) = (101,106,105)
    """
    pixels = img.load()
    width, height = img.size
    typ = 0

    for y in range(height):
        if typ >= len(ascii_vals):
            break
        for x in range(width):
            if typ >= len(ascii_vals):
                break
            r, g, b, a = pixels[x, y]
            r = (r // 10) * 10
            g = (g // 10) * 10
            b = (b // 10) * 10

            new_r = r + (ascii_vals[typ] % 10)
            new_g = g + ((ascii_vals[typ] // 10) % 10)
            new_b = b + ((ascii_vals[typ] // 100) % 10)

            if new_r >= 256:    # Least significant digit
                new_r -= 10
            if new_g >= 256:    # Second least significant digit
                new_g -= 10
            if new_b >= 256:    # Third least significant digit
                new_b -= 10

            pixels[x, y] = (new_r, new_g, new_b, a)
            typ += 1

    pixels[0, 0] = (0, 0, 0, 1)  # Indicator for color encoding

def transparency_decoding(img, pixels):
    '''
    transparency_decoding(image, pixel_array)
    Decodes the image sent to the method if it was encoded via transparency(alpha) encoding
    '''
    decoded_message = ""
    textfile = open("Output.txt", "w")
    width, height = img.size
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

def color_decoding(img,pixels):
    '''
    color_decoding(image, pixel_array)
    Decodes the image sent to the method if it was encoded via color(RGB) encoding
    '''
    decoded_message = ""
    textfile = open("Output.txt", "w")
    width, height = img.size
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

def main():
    """Main function to execute the encoding process."""
    encode_or_decode = input("Enter 1 to encode a message and 2 to decode a message: ")
    if(encode_or_decode == '1'):
        img = get_image()
        msg = get_message()
        ascii_vals = [ord(c) for c in msg]

        encoding_type = input("Enter 1 for transparency encoding and 2 for color encoding: ")
        if encoding_type == '1':
            transparency_encoding(img, ascii_vals)
        elif encoding_type == '2':
            color_encoding(img, ascii_vals)
        else:
            raise ValueError("Invalid encoding type")

        img.save("output.png")
        print("Image saved as output.png")
    elif(encode_or_decode == '2'):
        img = get_image()
        pixels = img.load()
        if pixels[0,0] == (0,0,0,0):
            print("Detected transparency encoding.")
            transparency_decoding(img, pixels)
        elif pixels[0,0] == (0,0,0,1):
            print("Detected color encoding.")
            color_decoding(img,pixels)

if __name__ == "__main__":
    main()
