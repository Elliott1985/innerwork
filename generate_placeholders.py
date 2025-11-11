"""
Generate placeholder audio and video files for Virtual Debbie
These are temporary files that will be replaced with real voice/video later
"""

import os
import struct
import wave

def create_silent_audio(filename, duration_seconds=3):
    """Create a silent WAV file (can be converted to MP3 later)"""
    sample_rate = 44100
    num_channels = 1
    sample_width = 2  # 16-bit audio
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        
        # Write silent frames
        num_frames = int(sample_rate * duration_seconds)
        for _ in range(num_frames):
            # Write a frame of silence (zero amplitude)
            wav_file.writeframes(struct.pack('h', 0))
    
    print(f"✓ Created: {filename}")

def create_simple_video_html5(filename, width=220, height=220, duration_seconds=5):
    """
    Create a simple animated gradient video using PIL/Pillow
    Falls back to creating an animated GIF if video creation fails
    """
    try:
        from PIL import Image, ImageDraw
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create frames for animation
        frames = []
        fps = 10
        total_frames = fps * duration_seconds
        
        for i in range(total_frames):
            # Create a frame with gradient background
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            # Animated gradient colors (lavender/rose cycle)
            progress = i / total_frames
            
            # Lavender to rose transition
            r = int(197 + (212 - 197) * abs(0.5 - progress) * 2)
            g = int(159 + (165 - 159) * abs(0.5 - progress) * 2)
            b = int(201 + (165 - 201) * abs(0.5 - progress) * 2)
            
            # Draw gradient circle (face)
            for y in range(height):
                for x in range(width):
                    # Distance from center
                    dx = x - width // 2
                    dy = y - height // 2
                    distance = (dx * dx + dy * dy) ** 0.5
                    
                    if distance < min(width, height) // 2.5:
                        # Inside circle - fill with color
                        pixel_brightness = 1 - (distance / (min(width, height) // 2.5)) * 0.3
                        pixel_r = int(r * pixel_brightness)
                        pixel_g = int(g * pixel_brightness)
                        pixel_b = int(b * pixel_brightness)
                        img.putpixel((x, y), (pixel_r, pixel_g, pixel_b))
                    else:
                        # Outside circle - beige background
                        img.putpixel((x, y), (248, 245, 242))
            
            # Add simple face features
            # Eyes (blinking animation)
            if i % (fps * 2) < fps * 1.8:  # Blink every 2 seconds
                eye_y = height // 2 - 20
                draw.ellipse([width // 2 - 40, eye_y - 5, width // 2 - 30, eye_y + 5], fill=(60, 60, 60))
                draw.ellipse([width // 2 + 30, eye_y - 5, width // 2 + 40, eye_y + 5], fill=(60, 60, 60))
            
            # Smile
            smile_y = height // 2 + 15
            draw.arc([width // 2 - 30, smile_y, width // 2 + 30, smile_y + 30], 0, 180, fill=(212, 165, 165), width=3)
            
            frames.append(img)
        
        # Save as GIF (fallback if video encoding fails)
        gif_filename = filename.replace('.mp4', '.gif').replace('.webm', '.gif')
        frames[0].save(
            gif_filename,
            save_all=True,
            append_images=frames[1:],
            duration=100,  # ms per frame
            loop=0
        )
        print(f"✓ Created animated GIF: {gif_filename}")
        
        # Note: For MP4, you would need additional libraries like opencv-python or moviepy
        # For now, we'll use the GIF as the primary avatar
        print(f"  Note: Using GIF format. For MP4, install: pip install opencv-python")
        
    except ImportError:
        print(f"✗ PIL/Pillow not installed. Run: pip install Pillow")
        print(f"  Creating simple placeholder instructions file instead...")
        
        # Create a README instead
        readme_path = os.path.join(os.path.dirname(filename), 'README.txt')
        with open(readme_path, 'w') as f:
            f.write("PLACEHOLDER MEDIA FILES\n")
            f.write("=" * 50 + "\n\n")
            f.write("These files should be replaced with actual avatar media:\n\n")
            f.write("1. debbie_avatar.mp4 or .gif - Animated avatar video\n")
            f.write("2. debbie_line1.mp3 - Audio greeting files\n\n")
            f.write("For now, the system will work in 'subtitle-only' mode.\n")
            f.write("Audio files can be generated with ElevenLabs or recorded manually.\n")
        
        print(f"✓ Created README: {readme_path}")

# Create the placeholder files
media_dir = "static/media"

print("Generating placeholder media files for Virtual Debbie...\n")

# Create audio files (different durations for variety)
audio_files = [
    ("debbie_line1.wav", 3.5),  # "Welcome back — it's good to see you again."
    ("debbie_line2.wav", 3.0),  # "Remember: healing takes patience and gentleness."
    ("debbie_line3.wav", 3.5),  # "Let's take a moment to breathe before we continue."
    ("debbie_line4.wav", 2.5),  # "You're doing wonderful work today."
]

for filename, duration in audio_files:
    filepath = os.path.join(media_dir, filename)
    create_silent_audio(filepath, duration)

# Create video/GIF avatar
video_path = os.path.join(media_dir, "debbie_avatar.mp4")
create_simple_video_html5(video_path)

print("\n" + "=" * 50)
print("✅ Placeholder generation complete!")
print("=" * 50)
print("\nNEXT STEPS:")
print("1. Replace WAV files with MP3 using: lame or online converter")
print("2. Or use text-to-speech services like ElevenLabs")
print("3. For production, replace with actual avatar video")
print("\nFor now, the system will work with these placeholders.")
print("Audio may be silent, but subtitles will display correctly.")
