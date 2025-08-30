import os
from PIL import Image, ImageDraw

def create_simple_favicon():
    """Create a simple favicon with paint brush icon"""
    
    print("🎨 Creating favicon files...")
    
    # Create favicon directory
    favicon_dir = os.path.join('app', 'static', 'favicon')
    os.makedirs(favicon_dir, exist_ok=True)
    
    # Create simple paint brush icon
    def create_icon(size):
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        primary = (37, 99, 235)  # Blue
        accent = (245, 158, 11)  # Orange
        
        # Simple brush design
        center = size // 2
        brush_width = size // 3
        
        # Handle (blue rectangle)
        handle_height = int(size * 0.4)
        handle_width = brush_width // 2
        handle_x = center - handle_width // 2
        handle_y = center - handle_height // 2
        
        draw.rectangle([
            handle_x, handle_y,
            handle_x + handle_width, handle_y + handle_height
        ], fill=primary)
        
        # Brush tip (orange)
        tip_height = int(size * 0.3)
        tip_width = brush_width
        tip_x = center - tip_width // 2
        tip_y = handle_y + handle_height
        
        draw.rectangle([
            tip_x, tip_y,
            tip_x + tip_width, tip_y + tip_height
        ], fill=accent)
        
        return img
    
    # Generate all required sizes
    sizes = {
        16: 'favicon-16x16.png',
        32: 'favicon-32x32.png',
        180: 'apple-touch-icon.png',
        512: 'favicon.png'
    }
    
    for size, filename in sizes.items():
        icon = create_icon(size)
        icon.save(os.path.join(favicon_dir, filename))
        print(f"   ✅ Created: {filename}")
    
    # Create ICO file
    icon_32 = create_icon(32)
    icon_32.save(
        os.path.join(favicon_dir, 'favicon.ico'),
        format='ICO',
        sizes=[(32, 32)]
    )
    print(f"   ✅ Created: favicon.ico")
    
    # Create web manifest
    manifest = {
        "name": "Color&Craft",
        "short_name": "Color&Craft",
        "icons": [
            {
                "src": "/static/favicon/favicon-32x32.png",
                "sizes": "32x32",
                "type": "image/png"
            }
        ],
        "theme_color": "#2563eb",
        "background_color": "#ffffff",
        "display": "standalone"
    }
    
    import json
    with open(os.path.join(favicon_dir, 'site.webmanifest'), 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"   ✅ Created: site.webmanifest")
    print("\n🎉 All favicon files created successfully!")
    print(f"📂 Files saved to: {favicon_dir}")

if __name__ == '__main__':
    try:
        create_simple_favicon()
    except ImportError:
        print("❌ PIL (Pillow) not installed. Run: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")