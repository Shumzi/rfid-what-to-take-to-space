# RFID Image Display System

An interactive display system for museum exhibits that shows fullscreen images when RFID tags are scanned.

## Features

- **RFID-triggered image display**: Automatically displays images when RFID tags are scanned
- **Fullscreen display**: Optimized for kiosk mode with fullscreen interface
- **Automatic welcome screen**: Returns to welcome image after inactivity
- **Easy calibration**: Simple tool to map RFID codes to images
- **Keyboard emulation support**: Works with USB RFID readers that emulate keyboard input

## Installation

1. Clone or download this repository

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare your images:
   - Place image files in the `data/images/` directory
   - Supported formats: JPG, JPEG, PNG, GIF, BMP
   - Recommended: Use high-resolution images for best display quality

## Usage

### Step 1: Calibrate (Map RFID Tags to Images)

Before running the display, you need to map your RFID tags to images:

1. Run the calibration script:
   ```bash
   python -m src.calibrate
   ```

2. When prompted, scan an RFID tag with your reader
   - The RFID code will be detected automatically
   - A dialog will appear asking you to select an image

3. Select the image that should be displayed for that RFID tag
   - Choose from the dropdown menu
   - Click "Save Mapping"

4. Repeat for all RFID tags you want to use

5. Press `Ctrl+C` then `Enter` to exit calibration when done
   - Your mappings are automatically saved to `config.json`

### Step 2: Run the Display

1. Start the main display program:
   ```bash
   python -m src.main
   ```

2. The system will:
   - Display in fullscreen mode
   - Show the welcome image initially
   - Wait for RFID tag scans
   - Display the corresponding image when a tag is scanned
   - Return to welcome image after inactivity timeout

3. To exit:
   - Press `Escape` key

## Configuration

The system uses `config.json` for configuration. You can edit this file directly or it will be created automatically during calibration.

### Configuration Options

- **`rfid_mappings`**: Dictionary mapping RFID codes to image filenames
  ```json
  "rfid_mappings": {
    "123": "pear.jpg",
    "464": "apple.jpg"
  }
  ```

- **`inactivity_timeout`**: Time in seconds before returning to welcome image (default: 30)
  ```json
  "inactivity_timeout": 30
  ```

- **`welcome_image`**: Filename of the image to show initially and after inactivity (default: "welcome.jpg")
  ```json
  "welcome_image": "welcome.jpg"
  ```

## How It Works

1. **RFID Input**: The system captures keyboard input from USB RFID readers that emulate keyboard input
   - When you scan a tag, the reader sends the RFID code as keyboard characters followed by Enter
   - The system captures this input globally (works even if the window doesn't have focus)

2. **Image Display**: 
   - Images are automatically scaled to fit the screen while maintaining aspect ratio
   - Images are displayed fullscreen with black background

3. **Inactivity Timer**: 
   - After the configured timeout period, the system automatically returns to the welcome image
   - The timer resets each time a new RFID tag is scanned

## Troubleshooting

**RFID tags not being detected:**
- Make sure your RFID reader is connected and working
- Test the reader in a text editor to verify it's sending keyboard input
- Check that the reader sends characters followed by Enter key

**Images not displaying:**
- Verify image files are in `data/images/` directory
- Check that filenames in `config.json` match actual image filenames (case-sensitive)
- Ensure image files are in supported formats (JPG, PNG, GIF, BMP)

**Configuration file not found:**
- Run `calibrate.py` first to create the initial configuration
- Or manually create `config.json` with the structure shown above

**Window won't close:**
- Press `Escape` key to exit fullscreen mode
- If that doesn't work, use `Ctrl+C` in the terminal

## Project Structure

```
.
├── src/
│   ├── main.py          # Main display program
│   └── calibrate.py     # Calibration tool for mapping RFID tags
├── data/
│   └── images/          # Place your images here
├── config.json          # Configuration file (created during calibration)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- The system works with RFID readers that emulate keyboard input (most USB RFID readers)
- Images are scaled to fit the screen while maintaining aspect ratio
- The display runs in fullscreen kiosk mode - perfect for dedicated exhibit displays
- Press `Escape` to exit the application

