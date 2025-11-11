/**
 * Virtual Elliott - Voice Synchronization Demo
 * Three-part greeting sequence with synced subtitles
 */

document.addEventListener("DOMContentLoaded", function() {
  const playBtn = document.getElementById("playVoiceBtn");
  const subtitleBox = document.getElementById("elliottSubtitleBox");
  const elliottVideo = document.getElementById("elliottVideo");

  // Three-part greeting sequence
  const lines = [
    { 
      text: "Welcome back. Take a deep breath in—and out.", 
      audio: "/static/media/Greeting1.mp3" 
    },
    { 
      text: "Let's focus on one gentle step forward today.", 
      audio: "/static/media/Greeting2.mp3" 
    },
    { 
      text: "Relax your shoulders. You're doing great.", 
      audio: "/static/media/Micropractice.mp3" 
    }
  ];

  let current = 0;
  let isPlaying = false;
  const audio = new Audio();

  // Initialize
  if (subtitleBox) {
    subtitleBox.innerText = "Ready to begin.";
  }

  // Play button handler
  if (playBtn) {
    playBtn.addEventListener("click", () => {
      if (isPlaying) {
        stopPlayback();
      } else {
        startPlayback();
      }
    });
  }

  function startPlayback() {
    isPlaying = true;
    
    // Update button
    playBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pause-fill me-2" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg> Pause Demo';
    playBtn.classList.remove('btn-outline-primary');
    playBtn.classList.add('btn-primary');
    
    // Visual feedback on video
    if (elliottVideo) {
      // Keep video muted - only play the audio files
      if (elliottVideo.tagName === 'VIDEO') {
        elliottVideo.muted = true; // Keep muted, we're using separate audio files
      }
      elliottVideo.style.transform = 'scale(1.05)';
      elliottVideo.style.transition = 'transform 0.3s ease';
    }
    
    current = 0;
    playLine();
  }

  function stopPlayback() {
    isPlaying = false;
    audio.pause();
    audio.currentTime = 0;
    
    // Reset button
    playBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-fill me-2" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg> Play Voice Demo';
    playBtn.classList.remove('btn-primary');
    playBtn.classList.add('btn-outline-primary');
    
    if (subtitleBox) {
      subtitleBox.innerText = "Ready to begin.";
    }
    
    // Reset video
    if (elliottVideo) {
      if (elliottVideo.tagName === 'VIDEO') {
        elliottVideo.muted = true;
      }
      elliottVideo.style.transform = 'scale(1)';
    }
  }

  function playLine() {
    if (!isPlaying) return;
    
    const line = lines[current];
    
    // Fade in subtitle
    if (subtitleBox) {
      subtitleBox.style.opacity = '0';
      subtitleBox.innerText = `"${line.text}"`;
      
      setTimeout(() => {
        subtitleBox.style.opacity = '1';
      }, 100);
    }
    
    // Stop any previous audio and play new audio
    audio.pause();
    audio.currentTime = 0;
    audio.src = line.audio;
    audio.play().catch(err => {
      console.error('Audio playback failed:', err);
      // Continue with subtitle-only mode
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
      // All lines complete - loop back or stop
      setTimeout(() => {
        current = 0;
        if (isPlaying) {
          playLine(); // Loop the sequence
        }
      }, 3000); // 3 second pause before looping
    } else {
      // Play next line after pause
      setTimeout(() => {
        if (isPlaying) {
          playLine();
        }
      }, 2000); // 2 second gap between lines
    }
  }

  // Handle audio errors gracefully
  audio.addEventListener('error', (e) => {
    console.error('Audio error:', e);
    if (subtitleBox) {
      subtitleBox.innerText = "Audio unavailable - showing subtitles only";
    }
    // Continue with visual-only mode
    scheduleNextLine();
  });
});

/**
 * IMPLEMENTATION NOTES:
 * 
 * 1. Three-line sequence loops continuously when playing
 * 2. 2-second pause between lines, 3-second pause before loop
 * 3. Works with both <video> and <img> avatar elements
 * 4. Graceful degradation to subtitle-only mode if audio fails
 * 5. Can be used alongside Virtual Debbie without conflicts
 * 
 * UPGRADE PATH:
 * - Replace .wav with .mp3 from ElevenLabs
 * - Add more greeting variations
 * - Implement context-aware greetings
 * - Integrate with lesson progress tracking
 */
