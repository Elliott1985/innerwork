"""
Generate placeholder media files for Virtual Elliott
Three greeting audio files + animated avatar
"""

import os
import struct
import wave

def create_silent_audio(filename, duration_seconds=3):
    """Create a silent WAV file"""
    sample_rate = 44100
    num_channels = 1
    sample_width = 2
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        
        num_frames = int(sample_rate * duration_seconds)
        for _ in range(num_frames):
            wav_file.writeframes(struct.pack('h', 0))
    
    print(f"✓ Created: {filename}")

def create_elliott_avatar(filename, width=220, height=220, duration_seconds=5):
    """Create animated Elliott avatar with blue/tech theme"""
    try:
        from PIL import Image, ImageDraw
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        frames = []
        fps = 10
        total_frames = fps * duration_seconds
        
        for i in range(total_frames):
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            # Blue gradient animation (tech theme)
            progress = i / total_frames
            
            # Cycle between light blue and darker blue
            r = int(100 + (140 - 100) * abs(0.5 - progress) * 2)
            g = int(150 + (180 - 150) * abs(0.5 - progress) * 2)
            b = int(200 + (220 - 200) * abs(0.5 - progress) * 2)
            
            # Draw gradient circle (face)
            for y in range(height):
                for x in range(width):
                    dx = x - width // 2
                    dy = y - height // 2
                    distance = (dx * dx + dy * dy) ** 0.5
                    
                    if distance < min(width, height) // 2.5:
                        # Inside circle - blue gradient
                        pixel_brightness = 1 - (distance / (min(width, height) // 2.5)) * 0.3
                        pixel_r = int(r * pixel_brightness)
                        pixel_g = int(g * pixel_brightness)
                        pixel_b = int(b * pixel_brightness)
                        img.putpixel((x, y), (pixel_r, pixel_g, pixel_b))
                    else:
                        # Outside - light blue background
                        img.putpixel((x, y), (232, 244, 248))
            
            # Eyes (blinking)
            if i % (fps * 3) < fps * 2.7:  # Blink every 3 seconds
                eye_y = height // 2 - 20
                draw.ellipse([width // 2 - 40, eye_y - 5, width // 2 - 30, eye_y + 5], fill=(40, 60, 80))
                draw.ellipse([width // 2 + 30, eye_y - 5, width // 2 + 40, eye_y + 5], fill=(40, 60, 80))
            
            # Smile (tech-friendly)
            smile_y = height // 2 + 15
            draw.arc([width // 2 - 30, smile_y, width // 2 + 30, smile_y + 30], 0, 180, fill=(80, 120, 160), width=3)
            
            # Add subtle "tech" indicator (small dot - like recording indicator)
            pulse = int(20 + 10 * abs(0.5 - (i % 20) / 20) * 2)
            draw.ellipse([width - 30, 20, width - 20, 30], fill=(80, 120, 160, pulse))
            
            frames.append(img)
        
        # Save as GIF
        gif_filename = filename.replace('.mp4', '.gif').replace('.webm', '.gif')
        frames[0].save(
            gif_filename,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        print(f"✓ Created animated GIF: {gif_filename}")
        
    except ImportError:
        print(f"✗ PIL/Pillow not installed.")
        print(f"  Run: pip install Pillow")
        
        # Create placeholder README
        readme_path = os.path.join(os.path.dirname(filename), 'ELLIOTT_README.txt')
        with open(readme_path, 'w') as f:
            f.write("VIRTUAL ELLIOTT PLACEHOLDER FILES\n")
            f.write("=" * 50 + "\n\n")
            f.write("Required files:\n")
            f.write("1. VirtualElliottIntro.mp4/.gif - Animated avatar\n")
            f.write("2. Greeting1.mp3 - 'Welcome back. Take a deep breath...'\n")
            f.write("3. Greeting2.mp3 - 'Let's focus on one gentle step...'\n")
            f.write("4. MicroPractice.mp3 - 'Relax your shoulders...'\n\n")
            f.write("Currently in subtitle-only mode.\n")
        
        print(f"✓ Created README: {readme_path}")

# Generate files
media_dir = "static/media"

print("Generating Virtual Elliott placeholder files...\n")

# Create 3 greeting audio files
audio_files = [
    ("Greeting1.wav", 3.5),      # "Welcome back. Take a deep breath in—and out."
    ("Greeting2.wav", 3.0),      # "Let's focus on one gentle step forward today."
    ("MicroPractice.wav", 2.5),  # "Relax your shoulders. You're doing great."
]

for filename, duration in audio_files:
    filepath = os.path.join(media_dir, filename)
    create_silent_audio(filepath, duration)

# Create avatar
avatar_path = os.path.join(media_dir, "VirtualElliottIntro.mp4")
create_elliott_avatar(avatar_path)

print("\n" + "=" * 50)
print("✅ Virtual Elliott placeholders complete!")
print("=" * 50)
print("\nFILES CREATED:")
print("• Greeting1.wav (3.5s)")
print("• Greeting2.wav (3.0s)")
print("• MicroPractice.wav (2.5s)")
print("• VirtualElliottIntro.gif (animated avatar)")
print("\nREADY TO TEST:")
print("1. Restart Flask server")
print("2. Navigate to any lesson page")
print("3. Virtual Elliott will appear in sidebar")
print("4. Click 'Play Voice Demo' to see it in action")
