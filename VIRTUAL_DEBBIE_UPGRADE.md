# Virtual Debbie - Voice Sync Upgrade Guide

## Current Implementation

The Virtual Debbie avatar currently uses:
- **Animated GIF** for visual representation (220x220px, looping)
- **WAV audio files** (silent placeholders)
- **Synced subtitles** displayed below avatar
- **Play/Pause controls** for greeting sequences

All components work **completely offline** with no external API dependencies.

---

## Placeholder Files

Located in `static/media/`:
```
debbie_avatar.gif        # Animated avatar (lavender/rose gradient face)
debbie_line1.wav         # "Welcome back — it's good to see you again."
debbie_line2.wav         # "Remember: healing takes patience and gentleness."
debbie_line3.wav         # "Let's take a moment to breathe before we continue."
debbie_line4.wav         # "You're doing wonderful work today."
```

---

## Upgrade Path to ElevenLabs (Voice Only)

### Step 1: Generate Voice Audio
```python
# Install ElevenLabs SDK
pip install elevenlabs

# Generate audio files
from elevenlabs import generate, save

lines = [
    "Welcome back — it's good to see you again.",
    "Remember: healing takes patience and gentleness.",
    "Let's take a moment to breathe before we continue.",
    "You're doing wonderful work today."
]

for i, text in enumerate(lines, 1):
    audio = generate(
        text=text,
        voice="Bella",  # Or create custom voice
        model="eleven_monolingual_v1"
    )
    save(audio, f"static/media/debbie_line{i}.mp3")
```

### Step 2: Update JavaScript
In `static/js/virtual_debbie.js`, change audio paths from `.wav` to `.mp3`:
```javascript
const lines = [
  { 
    text: "Welcome back — it's good to see you again.", 
    audio: "/static/media/debbie_line1.mp3"  // Changed from .wav
  },
  // ... rest of lines
];
```

**That's it!** The subtitle sync will work automatically with the real voice.

---

## Upgrade Path to D-ID (Talking Avatar)

### Step 1: Set up D-ID API
```python
# Install requests
pip install requests

# Create Flask route for D-ID integration
from flask import Blueprint, request, jsonify
import requests
import os

did_bp = Blueprint('did', __name__, url_prefix='/api/did')

@did_bp.route('/speak', methods=['POST'])
def create_talking_video():
    data = request.json
    text = data.get('text')
    
    # Call D-ID API
    response = requests.post(
        'https://api.d-id.com/talks',
        headers={
            'Authorization': f'Basic {os.getenv("DID_API_KEY")}',
            'Content-Type': 'application/json'
        },
        json={
            'script': {
                'type': 'text',
                'input': text,
                'provider': {
                    'type': 'microsoft',
                    'voice_id': 'en-US-JennyNeural'
                }
            },
            'source_url': 'https://yourdomain.com/static/media/debbie_portrait.jpg'
        }
    )
    
    video_data = response.json()
    return jsonify({
        'video_url': video_data['result_url'],
        'status': video_data['status']
    })
```

### Step 2: Update Frontend (virtual_debbie.html)
Replace the `<img>` with `<video>`:
```html
<video 
    id="debbieVideo" 
    autoplay 
    muted 
    loop 
    playsinline 
    width="220" 
    height="220" 
    style="border-radius: 12px; object-fit: cover;">
    <source src="/static/media/debbie_avatar.mp4" type="video/mp4">
</video>
```

### Step 3: Update JavaScript (virtual_debbie.js)
Add API call to fetch talking avatar:
```javascript
async function playLine() {
  if (!isPlaying) return;
  
  const line = lines[current];
  
  // Show subtitle
  subtitleBox.innerText = `"${line.text}"`;
  
  // Fetch D-ID talking video
  const response = await fetch('/api/did/speak', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: line.text })
  });
  
  const { video_url } = await response.json();
  
  // Update video source
  debbieVideo.src = video_url;
  debbieVideo.play();
  
  // Move to next line when video ends
  debbieVideo.onended = scheduleNextLine;
}
```

---

## Hybrid Approach (Best of Both)

Use **ElevenLabs for voice** + **static avatar video** for best quality/cost ratio:

1. Generate high-quality voice with ElevenLabs
2. Create one looping avatar video (MP4) with subtle movements
3. Sync voice audio with static video using current subtitle system

This avoids per-request D-ID costs while maintaining high quality.

---

## Testing the Current System

1. Start Flask app: `python app.py`
2. Navigate to any lesson page
3. Click "Play Greeting" in Virtual Debbie panel
4. Watch subtitles appear in sync with (silent) audio playback
5. Avatar will subtly scale up during playback

---

## File Structure

```
innerwork/
├── static/
│   ├── media/
│   │   ├── debbie_avatar.gif         # Current animated avatar
│   │   ├── debbie_avatar.mp4         # Future: talking head video
│   │   ├── debbie_line1.wav          # Replace with .mp3 from ElevenLabs
│   │   ├── debbie_line2.wav
│   │   ├── debbie_line3.wav
│   │   └── debbie_line4.wav
│   └── js/
│       └── virtual_debbie.js         # Voice sync logic
├── templates/
│   └── includes/
│       └── virtual_debbie.html       # Avatar component
└── VIRTUAL_DEBBIE_UPGRADE.md         # This file
```

---

## Cost Considerations

| Solution | Setup Cost | Per-Use Cost | Quality |
|----------|-----------|--------------|---------|
| Current (placeholders) | $0 | $0 | Low |
| ElevenLabs voice-only | ~$5/month | ~$0.001/char | High voice |
| D-ID talking avatar | ~$50/month | ~$0.10/video | Highest |
| Hybrid (ElevenLabs + static video) | ~$5/month | ~$0.001/char | High overall |

**Recommendation**: Start with ElevenLabs voice-only, upgrade to hybrid if needed.
