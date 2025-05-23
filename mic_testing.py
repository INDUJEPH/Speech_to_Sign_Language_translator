from PIL import Image

gif_path = r"E:\Python_projects\New folder\alphabet\h_small.gif"
try:
    img = Image.open(gif_path)
    img.show()
except FileNotFoundError:
    print(f"File not found: {gif_path}")
except Exception as e:
    print(f"Error: {e}")
