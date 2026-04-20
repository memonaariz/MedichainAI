"""Generate MediChain PWA icons"""
import os

def generate_icon(size, path):
    """Generate a simple SVG icon and save as PNG using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create gradient background
        img = Image.new('RGB', (size, size), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Draw gradient manually
        for y in range(size):
            ratio = y / size
            r = int(102 + (118 - 102) * ratio)
            g = int(126 + (75 - 126) * ratio)
            b = int(234 + (162 - 234) * ratio)
            draw.line([(0, y), (size, y)], fill=(r, g, b))
        
        # Draw rounded rectangle (card)
        margin = size // 6
        card_color = (255, 255, 255, 200)
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=size // 8,
            fill=(255, 255, 255, 180)
        )
        
        # Draw cross/medical symbol
        cx, cy = size // 2, size // 2
        bar_w = size // 8
        bar_h = size // 3
        
        # Vertical bar
        draw.rectangle([cx - bar_w//2, cy - bar_h//2, cx + bar_w//2, cy + bar_h//2], fill='#667eea')
        # Horizontal bar
        draw.rectangle([cx - bar_h//2, cy - bar_w//2, cx + bar_h//2, cy + bar_w//2], fill='#667eea')
        
        img.save(path, 'PNG')
        print(f"✅ Generated {path} ({size}x{size})")
        return True
    except ImportError:
        # Fallback: create minimal PNG without PIL
        create_minimal_png(size, path)
        return True

def create_minimal_png(size, path):
    """Create a minimal valid PNG icon"""
    import struct
    import zlib
    
    def png_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # Simple purple square PNG
    width = height = size
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    # Image data - purple gradient
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter type
        for x in range(width):
            # Purple color #667eea
            raw_data += bytes([102, 126, 234])
    
    compressed = zlib.compress(raw_data)
    
    png_data = (
        b'\x89PNG\r\n\x1a\n' +
        png_chunk(b'IHDR', ihdr_data) +
        png_chunk(b'IDAT', compressed) +
        png_chunk(b'IEND', b'')
    )
    
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f"✅ Generated minimal {path} ({size}x{size})")

if __name__ == '__main__':
    icons_dir = os.path.join(os.path.dirname(__file__), 'static', 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    generate_icon(192, os.path.join(icons_dir, 'icon-192.png'))
    generate_icon(512, os.path.join(icons_dir, 'icon-512.png'))
    
    print("\n✅ Icons generated successfully!")
    print("Now run: python app.py")
