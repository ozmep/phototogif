import os
import shutil
from PIL import Image, ImageDraw

# ask for folder path
folder = input("Enter folder path: ").strip().strip('"')

# output folder
output_folder = os.path.join(folder, "gifs")
os.makedirs(output_folder, exist_ok=True)

# supported formats
image_extensions = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif")
gif_extension = ".gif"

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        continue

    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        # case 1: already a GIF → move it
        if ext == gif_extension:
            dest = os.path.join(output_folder, filename)
            shutil.move(path, dest)
            print("Moved existing GIF:", filename)
            continue

        # case 2: image → convert to 2-frame GIF
        if ext in image_extensions:
            img = Image.open(path)

            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            frame1 = img.copy()

            frame2 = img.copy()
            draw = ImageDraw.Draw(frame2)

            # tiny pixel change
            x, y = 0, 0
            r, g, b = frame2.getpixel((x, y))[:3]
            draw.point((x, y), fill=((r + 1) % 256, g, b))

            output_path = os.path.join(output_folder, name + ".gif")

            frame1.save(
                output_path,
                save_all=True,
                append_images=[frame2],
                duration=1000,
                loop=0
            )

            print("Created:", name + ".gif")

    except Exception as e:
        print("Error with", filename, ":", e)

print("Done.")