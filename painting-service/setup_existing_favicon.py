import os
import shutil
from PIL import Image

def setup_favicon_from_existing(source_image_path):
    """Setup favicon from existing image file"""
    
    print(f"🎨 Setting up favicon from: {source_image_path}")
    
    if not os.path.exists(source_image_path):
        print(f"❌ Source image not found: {source_image_path}")
        return False
    
    # Create favicon directory
    favicon_dir = os.path.join('app', 'static', 'favicon')
    os.makedirs(favicon_dir, exist_ok=True)
    
    try:
        # Open source image
        with Image.open(source_image_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Generate different sizes
            sizes = [
                (16, 'favicon-16x16.png'),
                (32, 'favicon-32x32.png'),
                (180, 'apple-touch-icon.png'),
                (512, 'favicon.png')
            ]
            
            for size, filename in sizes:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                resized.save(os.path.join(favicon_dir, filename))
                print(f"   ✅ Created: {filename}")
            
            # Create ICO file
            img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
            img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
            
            img_16.save(
                os.path.join(favicon_dir, 'favicon.ico'),
                format='ICO',
                sizes=[(16, 16), (32, 32)]
            )
            print(f"   ✅ Created: favicon.ico")
            
        print("✅ Favicon setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False

if __name__ == '__main__':
    # Replace with your image path
    source_path = input("Enter path to your favicon image: ").strip()
    setup_favicon_from_existing(source_path)