import time
import threading
# import unicurses as uni
# import curses as cur
from curses import *
from unicurses import *

def spinning_animation(win, chars, delay, stop_event):
      while not stop_event.is_set():

        y, x = 7, 0
        for char in chars:
            win.addstr(x, y, char, color_pair(1))
            # win.prefresh()
            time.sleep(delay)
            win.refresh()
print("test 1")
def main(stdscr):
    # Initialize colors
    start_color()
    init_pair(1, COLOR_GREEN, COLOR_BLACK)

    # Define the characters and delays for the animation
    chars = "/-\|"
    delay = 0.1
    print("test")
    stop_event = threading.Event()
    thread = threading.Thread(target=spinning_animation, args=(stdscr, chars, delay, stop_event))

    try:
        thread.start()
        stdscr.getch()  # Wait for user input
        stop_event.set()
        thread.join()
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()

wrapper(main)