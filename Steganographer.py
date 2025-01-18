from PIL import Image
img_path = input("Enter your image file path: ")
img_path = img_path.strip('"')
print (img_path)
img = Image.open(img_path)
img = img.convert('RGBA')
width, height = img.size
#for y in range(height):
#    for x in range(width):
#        r, g, b, a = img.getpixel((x, y))
#        print(f"Pixel at ({x}, {y}) has ARGB values: ({r}, {g}, {b}, {a})")
choice = input("Enter 1 for string and 2 for file path ")
choice = int(choice)
if(choice == 1):
    msg = input("Enter string ")
    msg = " " + msg
if(choice == 2):
    msg = input("Enter your text file path: ")
    f = open(msg, "r")
    msg = f.read()
    msg = " " + msg
    print(msg)
#msg = open(r"C:\Users\Arii\Downloads\retard.txt", "r").read()
#msg = "Hello World"
msg+="&"
ascii = [ord(c) for c in msg]
pixels = img.load()
typ = 0
encoding_type = input("Enter 1 for transperency encoding and 2 for colour encoding: ")
if(encoding_type == '1'):
    print("Type 1")
    for y in range(height):
        if(typ > len(msg)):
            break
        for x in range(width):
            if(typ >= len(msg)):
                break
            # Get the current ARGB values
            r, g, b, a = pixels[x, y]
            # Modify the transperency value
            new_a = ascii[typ]
            new_r = r
            new_g = g
            new_b = b
            # Set the new pixel value
            pixels[x, y] = (new_r, new_g, new_b, new_a)
            typ += 1
elif(encoding_type == '2'):
    for y in range(height):
        if(typ > len(msg)):
            break
        for x in range(width):
            if(typ >= len(msg)):
                break
            # Get the current ARGB values
            r, g, b, a = pixels[x, y]
            # Quantize RGB values to the nearest 10
            a = a
            r = (r // 10) * 10
            g = (g // 10) * 10
            b = (b // 10) * 10
        # Embed ASCII values into RGB
            new_a = a
            new_r = r + (ascii[typ] % 10)  # Least significant digit
            if(new_r>256):
                new_r-=10
            new_g = g + ((ascii[typ] // 10) % 10)  # Second least significant digit
            if(new_g>256):
                new_g-=10
            new_b = b + ((ascii[typ] // 100) % 10)  # Third least significant digit
            if(new_b>256):
                new_b-=10
            # Set the new pixel value
            pixels[x, y] = (new_r, new_g, new_b, new_a)
            typ += 1
    pixels[0, 0] = (0, 0, 0, 1)
if(encoding_type == '1'):  # Transparency encoding
    pixels[0, 0] = (0, 0, 0, 0)
if(encoding_type == '2'):  # Colour encoding
    pixels[0, 0] = (0, 0, 0, 1)
img.save("Output.png")


