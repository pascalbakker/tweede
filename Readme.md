# Tweede

## An image slideshow for drawing.

Creator: Pascal Bakker


![Screenshot](screenshot.png)

Tweede [(1)](https://forvo.com/word/tweede/#nl) is a lightweight desktop application for artists to warm up. Execute tweede from your reference folder and it will rotate through every image at given time interval.

Similar websites for context:

http://reference.sketchdaily.net/

https://quickposes.com/en

https://line-of-action.com/

# Example

Cycles through pictures in a directory at a 60 second time interval.

    python tweede.py -p ~/Pictures/art_references -t 60

# Help

    usage: tweede.py [-h] -p PATHS [PATHS ...] [-r] [-t TIME] [-q] [-Q] [--bg_color BG_COLOR] [--fg_color FG_COLOR]
                 [--global_font GLOBAL_FONT] [--timer_font_size TIMER_FONT_SIZE] [--show_timer SHOW_TIMER]
                 [--arrows] [--no_arrows] [--allow_back ALLOW_BACK] [--disable_skip DISABLE_SKIP]
                 [--readjust_amount READJUST_AMOUNT]
		 
# TODO

	Add pause button

	Add class mode where users can set a time sequence. (I.e 5 images 30 seconds, 2 images 60 seconds, 1 image 500 seconds.)

	Add a gui start screen. Users will still be able to use the command line, but this streamlines the process for Windows users.
