# RFID Video Display
this tool simply wraps python-vlc to display videos based on the keycodes of rfid tags.  
usage flow:  
1. rfid reader reads disk
2. arduino translates read into a newline-terminated code
3. video_player_vlc.py displays video corresponding to code
4. welcome video loops infinitly after video ends.

calibration flow (done by operator when registering new disk):
1. operator writes `calibrate` and enters
2. disk read by rfid tag
3. operator chooses corresponding file to be shown
4. optionally sets the other side as well
5. optionally add another puck.
