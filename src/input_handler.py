#!/usr/bin/env python3
"""
RFID Input Handler for RFID Video Player.
Captures keyboard input and builds RFID codes from character sequences.
"""

import tkinter as tk


class InputHandler:
    """Handles RFID input capture from keyboard events."""
    
    def __init__(self, callback):
        """
        Initialize input handler.
        
        Args:
            callback: Function to call with RFID code string when Enter is pressed
        """
        self.callback = callback
        self.buffer = ""
        self.root = None
        self.listening = False
    
    def start(self, root):
        """
        Start listening for RFID input.
        
        Args:
            root: tkinter root window to bind keyboard events to
        """
        self.root = root
        self.listening = True
        self.buffer = ""
        
        # Bind keyboard events
        self.root.bind('<KeyPress>', self._on_key_press)
        self.root.focus_set()  # Ensure window can receive keyboard input
    
    def stop(self):
        """Stop listening for RFID input."""
        if self.root:
            self.root.unbind('<KeyPress>')
        self.listening = False
        self.buffer = ""
    
    def _on_key_press(self, event):
        """Handle key press events to build RFID code."""
        if not self.listening:
            return
        
        try:
            # Handle Enter key - process the RFID code
            if event.keysym == 'Return' or event.keysym == 'KP_Enter':
                if self.buffer:
                    rfid_code = self.buffer.strip()
                    self.buffer = ""  # Reset buffer
                    print(f"Received RFID code: {rfid_code}")
                    self.callback(rfid_code)
                return
            
            # Handle Escape key to exit
            if event.keysym == 'Escape':
                if self.root:
                    self.root.quit()
                return
            
            # Handle character keys - add to buffer
            if event.char and event.char.isprintable():
                self.buffer += event.char
        except Exception as e:
            print(f"Error handling key press: {e}")

