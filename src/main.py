#!/usr/bin/env python3
"""
Main application for RFID Video Player.
Orchestrates input handling, config loading, and video playback.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src directory to path for imports
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from config import load_config
from input_handler import InputHandler
from video_player import VideoPlayer


class RFIDVideoPlayer:
    """Main application orchestrating RFID input and video playback."""
    
    def __init__(self):
        """Initialize the application."""
        # Load configuration
        self.config = load_config()
        
        # Create video player
        self.player = VideoPlayer()
        
        # Create tkinter root window (minimal, just for input capture)
        self.root = tk.Tk()
        self.root.title("RFID Video Player")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        
        # Create input handler with callback
        self.input_handler = InputHandler(callback=self._handle_rfid_input)
        self.input_handler.start(self.root)
        
        # Bind Escape to quit
        self.root.bind('<Escape>', lambda e: self.quit())
    
    def _handle_rfid_input(self, rfid_code):
        """Handle RFID code input - lookup video and play it."""
        mappings = self.config.get("rfid_mappings", {})
        
        if rfid_code in mappings:
            video_filename = mappings[rfid_code]
            print(f"RFID {rfid_code} -> Playing video: {video_filename}")
            self.player.play(video_filename)
        else:
            print(f"RFID code {rfid_code} not found in mappings")
    
    def quit(self):
        """Quit the application."""
        self.player.stop()
        self.input_handler.stop()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the main application loop."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.quit()


def main():
    """Main entry point."""
    try:
        app = RFIDVideoPlayer()
        app.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
