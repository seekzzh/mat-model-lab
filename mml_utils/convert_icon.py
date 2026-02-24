from PIL import Image
import os

def convert():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, 'assets')
    png_path = os.path.join(assets_dir, 'icon.png')
    ico_path = os.path.join(assets_dir, 'icon.ico')
    
    if os.path.exists(png_path):
        img = Image.open(png_path)
        img.save(ico_path, format='ICO', sizes=[(256, 256)])
        print(f"Converted {png_path} to {ico_path}")
    else:
        print(f"Error: {png_path} not found")

if __name__ == "__main__":
    convert()
