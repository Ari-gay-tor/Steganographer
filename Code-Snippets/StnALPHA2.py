from PIL import Image

def get_message_input():
    choice = int(input("Enter 1 for string and 2 for file path: "))
    if choice == 1:
        return input("Enter string: ") + "&"
    elif choice == 2:
        file_path = input("Enter your text file path: ")
        with open(file_path, "r") as file:
            return file.read() + "&"
    return ""

def encode_message(image, message, encoding_type):
    width, height = image.size
    pixels = image.load()
    ascii_values = [ord(c) for c in message]
    typ = 0

    if encoding_type == 1:  # Transparency encoding
        for y in range(height):
            if typ >= len(message):
                break
            for x in range(width):
                if typ >= len(message):
                    break
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, ascii_values[typ])
                typ += 1
        pixels[0, 0] = (0, 0, 0, 0)  # End of message signal
    elif encoding_type == 2:  # Color encoding
        for y in range(height):
            if typ >= len(message):
                break
            for x in range(width):
                if typ >= len(message):
                    break
                r, g, b, a = pixels[x, y]
                r = (r // 10) * 10
                g = (g // 10) * 10
                b = (b // 10) * 10
                new_r = r + (ascii_values[typ] % 10)
                new_g = g + ((ascii_values[typ] // 10) % 10)
                new_b = b + ((ascii_values[typ] // 100) % 10)
                if new_r > 255: new_r -= 10
                if new_g > 255: new_g -= 10
                if new_b > 255: new_b -= 10
                pixels[x, y] = (new_r, new_g, new_b, a)
                typ += 1
        pixels[0, 0] = (0, 0, 0, 1)  # End of message signal

    return image

def main():
    img_path = input("Enter your image file path: ")
    img = Image.open(img_path).convert('RGBA')

    message = get_message_input()
    encoding_type = int(input("Enter 1 for transparency encoding and 2 for color encoding: "))
    
    img = encode_message(img, message, encoding_type)
    img.save("Output.png")

if __name__ == "__main__":
    main()
