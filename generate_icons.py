from PIL import Image, ImageDraw, ImageFont
import os

# Create icons directory if it doesn't exist
os.makedirs('icons', exist_ok=True)

# Icon sizes needed
icon_sizes = [72, 96, 120, 128, 144, 152, 167, 180, 192, 384, 512]

def create_icon(size):
    """Create an icon with gradient background and emoji"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(size):
        # Gradient from #667eea to #764ba2
        r = int(102 + (118 - 102) * y / size)
        g = int(126 + (75 - 126) * y / size)
        b = int(234 + (162 - 234) * y / size)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Draw rounded corners (iOS style)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    corner_radius = int(size * 0.2)
    mask_draw.rounded_rectangle([0, 0, size, size], radius=corner_radius, fill=255)
    
    # Apply mask
    img.putalpha(mask)
    
    # Add pregnancy emoji in center
    try:
        # Try to use system font, fallback to default
        font_size = int(size * 0.5)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Get text bbox for centering
        bbox = draw.textbbox((0, 0), "🤰", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - text_height // 4
        
        draw.text((x, y), "🤰", font=font, fill=(255, 255, 255, 255))
    except Exception as e:
        print(f"Warning: Could not add emoji to icon-{size}.png: {e}")
        # Draw a simple circle as fallback
        draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], fill=(255, 255, 255, 200))
    
    return img

def create_splash(width, height):
    """Create a splash screen"""
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        r = int(102 + (118 - 102) * y / height)
        g = int(126 + (75 - 126) * y / height)
        b = int(234 + (162 - 234) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # Add emoji
    try:
        font_size = int(width * 0.2)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Emoji
        bbox = draw.textbbox((0, 0), "🤰", font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - width * 0.1
        draw.text((x, y), "🤰", font=font, fill=(255, 255, 255, 255))
        
        # Title
        title_font_size = int(width * 0.06)
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", title_font_size)
        except:
            try:
                title_font = ImageFont.truetype("arial.ttf", title_font_size)
            except:
                title_font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), "Kontrakcie", font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + width * 0.15
        draw.text((x, y), "Kontrakcie", font=title_font, fill=(255, 255, 255, 255))
        
        # Subtitle
        subtitle_font_size = int(width * 0.04)
        try:
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", subtitle_font_size)
        except:
            try:
                subtitle_font = ImageFont.truetype("arial.ttf", subtitle_font_size)
            except:
                subtitle_font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), "Sledovanie pôrodu", font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + width * 0.22
        draw.text((x, y), "Sledovanie pôrodu", font=subtitle_font, fill=(255, 255, 255, 230))
        
    except Exception as e:
        print(f"Warning: Could not add text to splash screen: {e}")
    
    return img

print("Generating icons...")
for size in icon_sizes:
    icon = create_icon(size)
    icon.save(f'icon-{size}.png', 'PNG')
    print(f"  OK Created icon-{size}.png")

print("\nGenerating splash screens...")
splash_screens = [
    (640, 1136, 'splash-640x1136'),
    (750, 1334, 'splash-750x1334'),
    (1242, 2208, 'splash-1242x2208'),
    (1125, 2436, 'splash-1125x2436'),
    (828, 1792, 'splash-828x1792'),
    (1242, 2688, 'splash-1242x2688'),
]

for width, height, name in splash_screens:
    splash = create_splash(width, height)
    splash.save(f'{name}.png', 'PNG')
    print(f"  OK Created {name}.png")

print("\n[OK] All icons and splash screens generated successfully!")
print("\nFiles created:")
print("Icons: " + ", ".join([f"icon-{s}.png" for s in icon_sizes]))
print("Splash screens: " + ", ".join([s[2] + ".png" for s in splash_screens]))