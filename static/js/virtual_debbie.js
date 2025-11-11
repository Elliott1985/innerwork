/**
 * Virtual Debbie - Voice Sync & Subtitle System
 * Manages audio playback with synchronized subtitles
 * Easy to upgrade to ElevenLabs or D-ID API later
 */

document.addEventListener("DOMContentLoaded", function() {
  const speakBtn = document.getElementById("speakBtn");
  const subtitleBox = document.getElementById("subtitleBox");
  const debbieVideo = document.getElementById("debbieVideo");

  // Greeting lines with audio paths (ready for API replacement)
  const lines = [
    { 
      text: "Welcome back — it's good to see you again.", 
      audio: "/static/media/debbie_line1.wav" 
    },
    { 
      text: "Remember: healing takes patience and gentleness.", 
      audio: "/static/media/debbie_line2.wav" 
    },
    { 
      text: "Let's take a moment to breathe before we continue.", 
      audio: "/static/media/debbie_line3.wav" 
    },
    { 
      text: "You're doing wonderful work today.", 
      audio: "/static/media/debbie_line4.wav" 
    }
  ];

  let current = 0;
  let isPlaying = false;
  const audio = new Audio();

  // Initialize
  if (subtitleBox) {
    subtitleBox.innerText = "Ready to begin...";
  }

  // Play button handler
  if (speakBtn) {
    speakBtn.addEventListener("click", () => {
      if (isPlaying) {
        stopPlayback();
      } else {
        startPlayback();
      }
    });
  }

  function startPlayback() {
    isPlaying = true;
    speakBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pause-fill me-2" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg> Pause';
    speakBtn.classList.remove('btn-outline-primary');
    speakBtn.classList.add('btn-primary');
    
    // Visual feedback (works for both img and video)
    if (debbieVideo) {
      // If it's a video element, unmute it
      if (debbieVideo.tagName === 'VIDEO') {
        debbieVideo.muted = false;
        debbieVideo.volume = 0.3; // Keep low since audio is separate
      }
      // Add subtle animation to avatar during playback
      debbieVideo.style.transform = 'scale(1.05)';
      debbieVideo.style.transition = 'transform 0.3s ease';
    }
    
    current = 0;
    playLine();
  }

  function stopPlayback() {
    isPlaying = false;
    audio.pause();
    audio.currentTime = 0;
    
    speakBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-fill me-2" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg> Play Greeting';
    speakBtn.classList.remove('btn-primary');
    speakBtn.classList.add('btn-outline-primary');
    
    if (subtitleBox) {
      subtitleBox.innerText = "Ready to begin...";
    }
    
    // Reset video/avatar
    if (debbieVideo) {
      if (debbieVideo.tagName === 'VIDEO') {
        debbieVideo.muted = true;
      }
      // Reset scale animation
      debbieVideo.style.transform = 'scale(1)';
    }
  }

  function playLine() {
    if (!isPlaying) return;
    
    const line = lines[current];
    
    // Show subtitle with fade-in effect
    if (subtitleBox) {
      subtitleBox.style.opacity = '0';
      subtitleBox.innerText = `"${line.text}"`;
      
      setTimeout(() => {
        subtitleBox.style.opacity = '1';
      }, 100);
    }
    
    // Play audio
    audio.src = line.audio;
    audio.play().catch(err => {
      console.error('Audio playback failed:', err);
      // Fallback: continue to next line even if audio fails
      scheduleNextLine();
    });
  }

  // When audio ends, move to next line
  audio.addEventListener('ended', () => {
    scheduleNextLine();
  });

  function scheduleNextLine() {
    if (!isPlaying) return;
    
    current++;
    
    if (current >= lines.length) {
      // All lines complete - stop playback
      setTimeout(() => {
        stopPlayback();
      }, 2000); // Small delay before stopping
    } else {
      // Play next line after a brief pause
      setTimeout(() => {
        if (isPlaying) {
          playLine();
        }
      }, 1500); // 1.5 second gap between lines
    }
  }

  // Handle errors
  audio.addEventListener('error', (e) => {
    console.error('Audio error:', e);
    if (subtitleBox) {
      subtitleBox.innerText = "Audio unavailable - using subtitles only";
    }
    // Continue with visual-only mode
    scheduleNextLine();
  });
});

/**
 * UPGRADE PATH TO ELEVENLABS/D-ID:
 * 
 * 1. Replace lines array with API endpoint:
 *    const response = await fetch('/api/debbie/speak', {
 *      method: 'POST',
 *      body: JSON.stringify({ text: line.text })
 *    });
 *    const { audioUrl, videoUrl } = await response.json();
 * 
 * 2. For D-ID, replace video source dynamically:
 *    debbieVideo.src = videoUrl;
 * 
 * 3. For ElevenLabs voice-only:
 *    Keep current video, just replace audio.src with API response
 * 
 * 4. Add caching layer to avoid regenerating on each play
 */
