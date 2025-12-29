#!/usr/bin/env python3
"""
Video Player for RFID Video Player.
Plays videos using VLC subprocess with hardware acceleration.
"""

import os
import subprocess
import threading
from pathlib import Path


class VideoPlayer:
    """Plays videos using VLC subprocess in a separate thread."""
    
    def __init__(self, media_dir="data/images"):
        """
        Initialize video player.
        
        Args:
            media_dir: Directory containing video files
        """
        self.media_dir = Path(media_dir)
        self.current_process = None
        self.lock = threading.Lock()
        self._is_playing = False
    
    def play(self, video_filename):
        """
        Play a video file.
        
        Args:
            video_filename: Name of video file (relative to media_dir)
        
        Returns:
            bool: True if video started successfully, False otherwise
        """
        video_path = self.media_dir / video_filename
        
        if not video_path.exists():
            print(f"Warning: Video not found: {video_path}")
            return False
        
        # Stop any currently playing video
        self.stop()
        
        # Check if running on Raspberry Pi for hardware acceleration
        is_raspberry_pi = self._is_raspberry_pi()
        
        try:
            if is_raspberry_pi:
                # Use hardware acceleration on Raspberry Pi
                vlc_cmd = [
                    'vlc',
                    '--fullscreen',
                    '--no-osd',
                    '--quiet',
                    '--intf', 'dummy',
                    '--mmal-vout',  # Hardware accelerated video output
                    '--mmal-hw-dec',  # Hardware decoding
                    '--no-video-title-show',
                    str(video_path)
                ]
            else:
                # Standard VLC for other systems
                vlc_cmd = [
                    'vlc',
                    '--fullscreen',
                    '--no-osd',
                    '--quiet',
                    '--intf', 'dummy',
                    '--no-video-title-show',
                    str(video_path)
                ]
            
            print(f"Playing video: {video_path}")
            
            # Start VLC in subprocess
            with self.lock:
                self.current_process = subprocess.Popen(vlc_cmd)
                self._is_playing = True
            
            # Monitor process in background thread
            monitor_thread = threading.Thread(
                target=self._monitor_process,
                args=(self.current_process,),
                daemon=True
            )
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting video playback: {e}")
            with self.lock:
                self._is_playing = False
            return False
    
    def stop(self):
        """Stop currently playing video."""
        with self.lock:
            if self.current_process is not None:
                try:
                    self.current_process.terminate()
                    self.current_process.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    try:
                        self.current_process.kill()
                    except:
                        pass
                except Exception as e:
                    print(f"Error stopping video: {e}")
                finally:
                    self.current_process = None
                    self._is_playing = False
    
    def is_playing(self):
        """Check if a video is currently playing."""
        with self.lock:
            return self._is_playing
    
    def _monitor_process(self, process):
        """Monitor video process and update playing state when finished."""
        try:
            process.wait()
        except Exception as e:
            print(f"Error monitoring video process: {e}")
        finally:
            with self.lock:
                if self.current_process == process:
                    self.current_process = None
                    self._is_playing = False
    
    def _is_raspberry_pi(self):
        """Check if running on Raspberry Pi."""
        try:
            if os.path.exists('/proc/device-tree/model'):
                with open('/proc/device-tree/model', 'r') as f:
                    model = f.read()
                    return 'Raspberry Pi' in model
        except:
            pass
        return False

